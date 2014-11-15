# builtin
import logging

# config
from config import shared_config

# third party
import redis


logger = logging.getLogger(shared_config.api_log_root_name + __name__)
pipe = redis.StrictRedis(host=shared_config.redis_host).pipeline()


def keys():
    results = pipe.keys("*").execute()[0]
    try:
        if results:
            logger.debug("returning all names with details")
            for name in results: pipe.object(infotype="encoding", key=name)

            key_types = pipe.execute()

            for r in results: pipe.execute_command("TTL", r)

            k_tt = pipe.execute()

            names = [{"encoding": ktyp, "name": knam, "ttl": ktt} for ktyp, knam, ktt in zip(key_types, results, k_tt)]
        else:
            names = None
        return names
    except Exception as e:
        logger.error("failed to return key list because %s" % e, exc_info=True)
        raise RuntimeError("failed to return key list because %s" % e)