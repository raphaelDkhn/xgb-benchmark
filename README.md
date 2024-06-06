# ZKBoost Benchmark on Stone & Platinum

This repository provides benchmarks for XGBoost models across varying numbers of trees and depths. 

XGBoost models have been serialized in `serialized_models` directory. To reproduce these models, refer to the [Jupyter notebook](xgb.ipynb). 
After reproducing, you can use [Giza-CLI](https://docs.gizatech.xyz/products/platform/resources/transpile) to transpile the serialized models into Cairo.

## Performance Metrics

The table below summarizes the performance metrics for different configurations of the XGBoost model with two provers: Stone and Platinum.

Models are named following their configuration: number of trees and depth. For example, an XGBoost model with 5 trees and depth 4 is named `xgb_t5_d4`.

All benchmarks have been conducted on an `e2-highmem-4` machine, equipped with an Intel Broadwell CPU on x86/64 architecture.

| Model         | Steps (proof_mode) | Proving Time in Stone | Verifying Time in Stone | Proving Time in Platinum | Verifying Time in Platinum | Verifying Onchain |
| ------------- | ------------------ | --------------------- | ----------------------- | ------------------------ | -------------------------- | ----------------- |
| `xgb_t5_d4`   | 8192               | 0m16.732s             | 0m0.243s                | 0m1.851s                 | 0m0.038s                   | TODO              |
| `xgb_t5_d6`   | 8192               | 0m16.067s             | 0m0.294s                | 0m2.275s                 | 0m0.037s                   | TODO              |
| `xgb_t20_d6`  | 32768              | 1m1.727s              | 0m0.539s                | 0m7.069s                 | 0m0.119s                   | TODO              |
| `xgb_t70_d6`  | 131072             | 4m9.207s              | 0m1.163s                | 0m29.017s                | 0m0.465s                   | TODO              |
| `xgb_t200_d4` | 131072             | 4m9.312s              | 0m1.266s                | 0m29.871s                | 0m0.468s                   | TODO              |

## Stone 

First, install [Stone prover](https://github.com/starkware-libs/stone-prover), to run the following commands.

To prove a model run the following command:
```bash
MODEL=t5_d4 #Change the model here
time cpu_air_prover \
  --out_file=proofs/stone/xgb_${MODEL}_proof.json \
  --private_input_file=prover_inputs/xgb_${MODEL}/xgb_${MODEL}_private_input.json \
  --public_input_file=prover_inputs/xgb_${MODEL}/xgb_${MODEL}_public_input.json \
  --prover_config_file=prover_inputs/xgb_${MODEL}/cpu_air_prover_config.json \
  --parameter_file=prover_inputs/xgb_${MODEL}/cpu_air_params.json \
  --generate-annotations
```

To verify a model, run the following command
```bash
MODEL=t5_d4 #Change the model here
time cpu_air_verifier \
  --in_file=proofs/stone/xgb_${MODEL}_proof.json && echo "Successfully verified proof."
```

### How to calculate FRI steps?
The number of steps affects the size of the trace. Such changes may require modification of cpu_air_params.json. Specifically, the following equation must be satisfied.
```
log₂(last_layer_degree_bound) + ∑fri_step_list = log₂(#steps) + 4
```

You can run the `calculate_fri_step_list.py` script to calculate the FRI step list for a given number of steps. 
For example, for a program with 8192 steps run the following command:
```bash
$ python calculate_fri_steps.py 8192
>>>
FRI Step List: [4, 4, 3]
```

## Platinum

First, install Platinum prover to run the following commands.
```bash
cargo install --features=cli,instruments,parallel --git https://github.com/lambdaclass/lambdaworks.git --rev fed12d6 cairo-platinum-prover
```

To prove a model run the following command:
```bash
MODEL=t5_d4 #Change the model here
time platinum-prover prove \
prover_inputs/xgb_${MODEL}/xgb_${MODEL}_trace.json \
prover_inputs/xgb_${MODEL}/xgb_${MODEL}_memory.json \
proofs/platinum/xgb_${MODEL}.proof 
```

To verify a model, run the following command:
```bash
MODEL=t5_d4 #Change the model here
time platinum-prover verify \
proofs/platinum/xgb_${MODEL}.proof 
```