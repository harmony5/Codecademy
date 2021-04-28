#! /usr/bin/env python3

import dataclasses as dc
import typing as tp


SALES_TAX = 8.8 / 100


@dc.dataclass
class ProductInfo:
    id_count: tp.ClassVar[int] = 0
    id: int = dc.field(init=False)
    name: str
    price: float
    description: str

    def __post_init__(self):
        self.id = ProductInfo.id_count
        ProductInfo.id_count += 1


@dc.dataclass
class InventoryItem:
    id_count: tp.ClassVar[int] = 0
    id: int = dc.field(init=False)
    product: ProductInfo
    count: int

    def __post_init__(self):
        self.id = InventoryItem.id_count
        InventoryItem.id_count += 1


@dc.dataclass
class Customer:
    id_count: tp.ClassVar[int] = 0
    id: int = dc.field(init=False)
    name: str
    items_purchased: tp.List[ProductInfo] = dc.field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(map(lambda p: p.price, self.items_purchased))

    @property
    def itemization(self) -> str:
        if len(items := self.items_purchased) > 0:
            return "\n".join(map(lambda item: item.description, items))
        else:
            return ""

    @property
    def current_tax(self) -> float:
        return self.total * SALES_TAX

    @property
    def check_out_total(self) -> float:
        return self.total + self.current_tax

    def __post_init__(self):
        self.id = Customer.id_count
        Customer.id_count += 1

    def buy_item(self, item_name: str):
        item: ProductInfo = dispatch_item(item_name)
        self.items_purchased.append(item)

    def print_receipt(self):
        print(f"Customer {self.name} Items:")
        print(self.itemization)
        print(f"\nCustomer {self.name} Total: {self.check_out_total:.2f}")


inventory: tp.List[InventoryItem] = {}


def add_to_inventory(item: InventoryItem):
    global inventory
    inventory[item.product.name] = item


def dispatch_item(item_name: str):
    global inventory
    if item := inventory.get(item_name, None):
        if item.count > 0:
            item.count -= 1
            return item.product
        else:
            print(f"The item '{item_name}' is sold out.")
    else:
        print(f"Item '{item_name}' not in inventory.")


add_to_inventory(
    InventoryItem(
        ProductInfo(
            "Lovely Loveseat",
            254.00,
            "Lovely Loveseat. Tufted polyester blend on wood. 32 inches high x 40 inches wide x 30 inches deep. Red or white.",
        ),
        45,
    )
)
add_to_inventory(
    InventoryItem(
        ProductInfo(
            "Stylish Settee",
            180.50,
            "Stylish Settee. Faux leather on birch. 29.50 inches high x 54.75 inches wide x 28 inches deep. Black.",
        ),
        20,
    )
)
add_to_inventory(
    InventoryItem(
        ProductInfo(
            "Luxurious Lamp",
            52.15,
            "Luxurious Lamp. Glass and iron. 36 inches tall. Brown with cream shade.",
        ),
        15,
    )
)


# Customer One
wan: Customer = Customer("One")
wan.buy_item("Lovely Loveseat")
wan.buy_item("Luxurious Lamp")

wan.print_receipt()
