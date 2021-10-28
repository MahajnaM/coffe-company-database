import sys


from Repository import repo
import printdb


class dto_activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = int(quantity)
        self.activator_id = activator_id
        self.date = date


def actionMain(args):
    filepath = args[1] 


    with open(filepath) as fp:
        lines = fp.readlines()
        for line in lines:
            words = line.split(", ")
            words = [word.strip() for word in words]

            activity = dto_activity(*words)
            quantity = activity.quantity
            product = repo.dao_products.find(activity.product_id)

            if (quantity != 0) or (product.quantity + quantity) >= 0:
                repo.dao_activities.insert(activity)
                product.quantity = product.quantity + quantity
                repo.dao_products.update(product.id, "quantity", product.quantity)


if __name__ == '__main__':
    actionMain(sys.argv)
    printdb.printdb()
    exit()
