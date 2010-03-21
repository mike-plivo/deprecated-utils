#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <pthread.h>
#include "asterisk/logger.h"
#include "asterisk/manager.h"

struct dtmfs_feature {
	char buffer[256];
	int pos;
	struct timeval now;
	const char *script;
	int intertimeout;
	char pattern[256];
	int active;
	char extras[256];
};


static int dtmf_feature_active(struct ast_channel *chan, struct dtmfs_feature *dfeature) {
	if (!dfeature->script || ast_strlen_zero(dfeature->script)) {
		ast_log(LOG_WARNING, "MeetmeDtmf: OFF (channel %s): MEETME_FEATURE_SCRIPT not found\n", chan->name);
		return 0;
	}
	if (!dfeature->pattern || ast_strlen_zero(dfeature->pattern)) {
		ast_log(LOG_WARNING, "MeetmeDtmf: OFF (channel %s): MEETME_FEATURE_PATTERN not found\n", chan->name);
		return 0;
	}
	ast_log(LOG_WARNING, "MeetmeDtmf: ON (channel %s)\n", chan->name);
	return 1;
}

struct command_data {
	char channelname[256];
	char conf[256];
	char dtmfs[256];
	char script[256];
	char extras[256];
	int usernum;
};

static void *command_thread(void *data) {
	sigset_t signal_set, old_set;
	int pid, x;
        struct command_data *tobj = data;
	char *argv[6];
	char tmp[256];

	snprintf(tmp, 256, "%s", tobj->script);
	argv[0] = ast_strdup(tmp);
	snprintf(tmp, 256, "%s", tobj->channelname);
	argv[1] = ast_strdup(tmp);
	snprintf(tmp, 256, "%s", tobj->dtmfs);
	argv[2] = ast_strdup(tmp);
	snprintf(tmp, 256, "%s", tobj->conf);
	argv[3] = ast_strdup(tmp);
	snprintf(tmp, 256, "%d", tobj->usernum);
	argv[4] = ast_strdup(tmp);
	snprintf(tmp, 256, "%s", tobj->extras);
	argv[5] = ast_strdup(tmp);
	argv[6] = NULL;

	bzero(tobj, sizeof(*tobj)); /*! \todo XXX for safety */
	free(tobj);

	ast_log(LOG_DEBUG, "MeetmeDtmf: Channel:%s Conf:%s Usernum:%s DtmfsPressed:%s Script:%s Extras:%s\n", argv[1], argv[3], argv[4], argv[2], argv[0], S_OR(argv[5], ""));

        /* Block SIGHUP during the fork - prevents a race */
        sigfillset(&signal_set);
        pthread_sigmask(SIG_BLOCK, &signal_set, &old_set);
        pid = fork();

	if (pid < 0) {
		ast_log(LOG_ERROR, "MeetmeDtmf: Channel:%s Cannot fork() !\n", tobj->channelname);
		return NULL;
	}

	if (!pid) {
		/* Child */
		ast_set_priority(0);

                /* Before we unblock our signals, return our trapped signals back to the defaults */
                signal(SIGHUP, SIG_DFL);
                signal(SIGCHLD, SIG_DFL);
                signal(SIGINT, SIG_DFL);
                signal(SIGURG, SIG_DFL);
                signal(SIGTERM, SIG_DFL);
                signal(SIGPIPE, SIG_DFL);
                signal(SIGXFSZ, SIG_DFL);

                /* unblock important signal handlers */
                if (pthread_sigmask(SIG_UNBLOCK, &signal_set, NULL)) {
                        ast_log(LOG_WARNING, "unable to unblock signals for MeetmeDtmf script: %s\n", strerror(errno));
                        _exit(1);
                }

		/* Close unused file descriptors */
                for (x=0;x<8192;x++) {
                        if (-1 != fcntl(x, F_GETFL)) {
                                close(x);
                        }
                }
                setpgid(0, getpid());

		execv(argv[0], argv);
		ast_log(LOG_ERROR, "MeetmeDtmf: Exec failed\n");
		_exit(1);
	}
	
	/* Parent */
	pthread_sigmask(SIG_SETMASK, &old_set, NULL);
	pid = wait(NULL);

        return NULL;
}


static void command_thread_launch(void *data) {
	pthread_t thread;
        pthread_attr_t attr;
        struct sched_param sched;

        pthread_attr_init(&attr);
        pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
        ast_pthread_create(&thread, &attr,command_thread, data);
        pthread_attr_destroy(&attr);
        memset(&sched, 0, sizeof(sched));
        pthread_setschedparam(thread, SCHED_RR, &sched);
}


static void send_manager_dtmf_event(struct ast_channel *chan, char *confno, int userno, char *dtmfs, const char *script, const char *extras, struct timeval now)
{
	manager_event(EVENT_FLAG_CALL, "MeetmeDtmf",
	      "Channel: %s\r\n"
	      "Uniqueid: %s\r\n"
	      "Meetme: %s\r\n"
	      "Usernum: %d\r\n"
	      "Dtmfs: %s\r\n"
	      "Script: %s\r\n"
	      "Extras: %s\r\n"
	      "TimeSec: %ld\r\n"
	      "TimeUsec: %ld\r\n",
	      chan->name, chan->uniqueid, confno, userno, dtmfs, script, S_OR(extras,"<Not Set>"), now.tv_sec, now.tv_usec);
}


static int dtmf_pattern_match(struct ast_channel *chan, struct dtmfs_feature *dfeature)
{
	int i;
	int res = 0;
	int len = strlen(dfeature->pattern);
	if (dfeature->pos < len) {
		if (option_debug > 5) {
			ast_log(LOG_DEBUG, "MeetmeDtmf: nothing to do: dtmf buffer '%s' length don't match pattern '%s' length on channel %s\n", dfeature->buffer, dfeature->pattern, chan->name);
		}
		return res;
	}

	for (i=0;i<=len;i++) {
		if (dfeature->pos < i) {
			if (option_debug > 5) {
				ast_log(LOG_DEBUG, "MeetmeDtmf: max dtmf length buffer '%s' reached at pos %d on channel %s\n", dfeature->buffer, i, chan->name);
			}
			break;
		}
		if ((dfeature->buffer[i] == '\0') || (dfeature->pattern[i] == '\0')) {
			if (option_debug > 5) {
				ast_log(LOG_DEBUG, "MeetmeDtmf: end of dtmf buffer '%s' or pattern '%s' at pos %d on channel %s\n", dfeature->buffer, dfeature->pattern, i, chan->name);
			}
			break;
		}
		if ((dfeature->buffer[i] == dfeature->pattern[i]) || (dfeature->pattern[i] == 'X')) {
			res = 1;
		} else {
			res = 0;
			break;
		}
	}
	if (res == 1) {
		ast_log(LOG_DEBUG, "MeetmeDtmf: '%s' match pattern '%s' on channel %s\n", dfeature->buffer, dfeature->pattern, chan->name);
	} else {
		if (option_debug > 5) {
			ast_log(LOG_DEBUG, "MeetmeDtmf: '%s' don't match pattern '%s' on channel %s\n", dfeature->buffer, dfeature->pattern, chan->name);
		}
	}
	return res;
}

static void meetme_catch_dtmfs(struct ast_channel *chan, char *confno, int userno, char dtmf, struct dtmfs_feature *dfeature)
{
	struct command_data *tobj;
	struct timeval now;

        now = ast_tvnow();

	/* If current dtmf was sent in time and not reaching max buffer, add it to buffer */
	if ((ast_tvdiff_ms(now, dfeature->now) <= dfeature->intertimeout) && (dfeature->pos < 256)){
		/* If buffer length is equal to pattern length, reset buffer */
		if (strlen(dfeature->buffer) == strlen(dfeature->pattern)) {
			ast_log(LOG_DEBUG, "MeetmeDtmf: reset buffer to '%c' (0) (max pattern length reached) on channel %s\n", dtmf, chan->name);
			dfeature->buffer[0] = dtmf;
			dfeature->buffer[1] = '\0';
			dfeature->pos = 1;
		} else {
			ast_log(LOG_DEBUG, "MeetmeDtmf: add '%c' (%d) to buffer (channel %s)\n", dtmf, dfeature->pos, chan->name);
			dfeature->buffer[dfeature->pos] = dtmf;
			dfeature->buffer[dfeature->pos+1] = '\0';
			dfeature->pos++;
		}
	/* If current dtmf was coming after time or max buffer reached, reset buffer */
	} else {
		ast_log(LOG_DEBUG, "MeetmeDtmf: set buffer to '%c' (0) (channel %s)\n", dtmf, chan->name);
		dfeature->buffer[0] = dtmf;
		dfeature->buffer[1] = '\0';
		dfeature->pos = 1;
	}

	/* update time */
	dfeature->now = now;

	if (option_debug > 5) {
		ast_log(LOG_DEBUG, "MeetmeDtmf: buffer is now '%s' (channel %s)\n", dfeature->buffer, chan->name);
	}

	if (dtmf_pattern_match(chan, dfeature) == 1) {
		ast_log(LOG_DEBUG, "MeetmeDtmf: buffer '%s' match '%s' (channel %s)\n", dfeature->buffer, dfeature->pattern, chan->name);
		send_manager_dtmf_event(chan, confno, userno, dfeature->buffer, dfeature->script, dfeature->extras, dfeature->now);
		tobj = ast_calloc(1, sizeof(struct command_data));
		if (!tobj) {
			ast_log(LOG_ERROR, "MeetmeDtmf: cannot launch thread (channel %s)\n", chan->name);
		} else {
			ast_copy_string(tobj->channelname, chan->name, 256);
			ast_copy_string(tobj->conf, confno, 256);
			ast_copy_string(tobj->dtmfs, dfeature->buffer, 256);
			ast_copy_string(tobj->script, dfeature->script, 256);
			ast_copy_string(tobj->extras, dfeature->extras, 256);
			tobj->usernum = userno;
			command_thread_launch(tobj);
		}
	}
	return;
}


