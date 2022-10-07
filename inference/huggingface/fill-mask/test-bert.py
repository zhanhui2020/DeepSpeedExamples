from transformers import pipeline
import transformers
import deepspeed
import torch
import os

# from transformers import pipeline
# unmasker = pipeline('fill-mask', model='bert-base-cased')
# unmasker("Hello I'm a [MASK] model.")

local_rank = int(os.getenv('LOCAL_RANK', '0'))
world_size = int(os.getenv('WORLD_SIZE', '4'))

pipe = pipeline('fill-mask', model='bert-base-uncased', device=local_rank)

pipe.model = deepspeed.init_inference(
    pipe.model,
    mp_size=world_size,
    dtype=torch.float,
    replace_with_kernel_inject=True
)

pipe.device = torch.device(f'cuda:{local_rank}')
output = pipe("Hello I'm a [MASK] model.")

if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
    print(output)
