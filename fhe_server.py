import json
import base64
from concrete import fhe 
from mongo_context import find_circuit, find_keys

def fhe_server_compute(eval_key_id: str, argb64s: [str]):
    k = find_keys(eval_key_id)
    c = k['circuit']
    
    print(c)

    configuration = fhe.Configuration().fork(**json.loads(c['config']))
    server = fhe.Server.create(c['mlir'], configuration, False)
    f = open(f"{eval_key_id}.eval", mode="rb")
    deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(f.read())
    f.close()
    #deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(k['evaluation_keys'])

    args = list(map(lambda a: fhe.Value.deserialize(base64.b64decode(a)),argb64s))
    result: fhe.Value = server.run(*args, evaluation_keys=deserialized_evaluation_keys)
    serialized_result: bytes = result.serialize()

    return [base64.b64encode(serialized_result).decode("ascii")]
