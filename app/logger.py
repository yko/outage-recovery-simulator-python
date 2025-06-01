from logdash import create_logdash

logdash = create_logdash({
    "api_key": "...", #TODO: load api key from configuration
})

logger = logdash.logger
