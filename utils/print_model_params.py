import argparse

from prettytable import PrettyTable
from transformers import MT5Model, MT5ForConditionalGeneration, AutoModel


def print_parameters(model):
    table = PrettyTable(["Modules", "Parameters"])
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        params = parameter.numel()
        table.add_row([name, params])
        total_params += params
    print(table)
    print(f"Total Trainable Params: {total_params}")

    print('Reference numbers: ')
    print('models/mt5-base: ', 582401280)
    print('sugoi: ', 350107648)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=str)
    args = parser.parse_args()

    model = AutoModel.from_pretrained(f'models/{args.m}')

    print_parameters(model)
