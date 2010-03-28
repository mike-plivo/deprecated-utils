#include "asterisk.h"
#include "asterisk/options.h"
#include "asterisk/logger.h"

#define ast_debug(level, ...) do {       \
        if (option_debug >= (level)) \
                ast_log(LOG_DEBUG, __VA_ARGS__); \
} while (0)

