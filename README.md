# Foodkart

Foodkart is a small CLI food delivery app developed using [poetry](https://python-poetry.org/) and [typer](https://typer.tiangolo.com/)

### Requirements

Requirements can be found [here](/requirements.md)

### Design and models

Models and design can be found [here](./design.md)

### Usage
==========

```python

foodkart

 Usage: foodkart [OPTIONS] COMMAND [ARGS]...

 Foodkart is a small food delivery CLI app

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                      │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.               │
│ --help                        Show this message and exit.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ customers                                                                                                                    │
│ menu                                                                                                                         │
│ orders                                                                                                                       │
│ restaurants 

## Adding customers

foodkart customers register Mary --phone XXXXXXXXX

## Adding restaurants

foodkart restaurants add Royal India  --capacity 20

## Adding menu to restaurants

foodkart menu add Chicken tandoori --price 100 --rest-id 4

## Listing restaurants

foodkart restaurants list

## Placing order

foodkart orders book --customer-id 2 --item Biryani --quantity 2  

## Marking order as delivered

foodkart orders deliver --order-id 3

## Listing orders

## For all customers
foodkart orders list

## For specific customers
foodkart orders list --customer-id 2

## Updating menu for restaurants

foodkart menu update 10 Royal Biryani --price 300 --rest-id 1

```

### How to setup and run
- Install poetry from [here](https://python-poetry.org/docs/)
- Git clone the repo
- Go to repo directory and run these commands
    ```shell
    poetry install
    poetry shell
    ```
- Start running off the cli commands.
