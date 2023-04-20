import os

import click


def mkdir_baiduyun_dir(baiduyun_dir):
    """Create a directory in the baiduyun directory"""
    os.system("baidupcs-go mkdir %s" % baiduyun_dir)


def del_baiduyun_dir(baiduyun_dir):
    """Delete the directory in the baiduyun directory"""
    os.system("baidupcs-go rm %s/data" % baiduyun_dir)


def upload_baiduyun_dir(local_dir, baiduyun_dir):
    """Upload the directory to the baiduyun directory"""
    os.system("baidupcs-go upload %s %s" % (local_dir, baiduyun_dir))


def download_baiduyun_dir(baiduyun_dir):
    """Download the directory from the baiduyun directory"""
    os.system("baidupcs-go download %s/data ./" % baiduyun_dir)


@click.group()
def data_sync():
    pass


@click.command()
@click.option(
    "--baiduyun_dir",
    default="/data/Comparative-Study-of-Methods-for-Drive-Time-Estimation",
    help="Init the baiduyun_dir",
)
def init(baiduyun_dir):
    """Create a directory in the baiduyun directory"""
    mkdir_baiduyun_dir("/data/%s/data" % baiduyun_dir)


@click.command()
@click.option("--local_dir", default="./data", help="The local directory")
@click.option(
    "--baiduyun_dir",
    default="/data/Comparative-Study-of-Methods-for-Drive-Time-Estimation",
    help="The baiduyun directory",
)
def push_all(local_dir, baiduyun_dir):
    """Synchronize data to the baiduyun directory"""
    # mkdir_baiduyun_dir(baiduyun_dir)
    del_baiduyun_dir(baiduyun_dir)
    upload_baiduyun_dir(local_dir, baiduyun_dir)
    # download_baiduyun_dir()


@click.command()
@click.option("--local_dir", default="./data", help="The local directory")
@click.option(
    "--baiduyun_dir",
    default="/data/Comparative-Study-of-Methods-for-Drive-Time-Estimation",
    help="The baiduyun directory",
)
def pull_all(baiduyun_dir):
    """Synchronize data from the baiduyun directory"""
    download_baiduyun_dir(baiduyun_dir)


data_sync.add_command(push_all)
data_sync.add_command(pull_all)


if __name__ == "__main__":
    data_sync()
