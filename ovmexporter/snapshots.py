import os

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command

from ovmexporter import client


class ListSnapshots(Lister):

    def get_parser(self, prog_name):
        parser = super(ListSnapshots, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        snapshots = cli.get_snapshots(args.vmID)
        ret = [
            ["Snapshot ID",]
        ]
        items = []
        for snap in snapshots:
            item = [
                snap["id"],
            ]
            items.append(item)

        ret.append(items)
        return ret


class CreateSnapshot(ShowOne):

    def get_parser(self, prog_name):
        parser = super(CreateSnapshot, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        snap = cli.create_snapshot(args.vmID)
        columns = ('Snapshot ID',
                   'VM ID',
                   'Disks')

        data = (
            snap["id"],
            snap["vm_id"],
            "\n".join(
                [d["name"] for d in snap["disks"]]
            )
        )
        return (columns, data)


class ShowSnapshot(ShowOne):

    def get_parser(self, prog_name):
        parser = super(ShowSnapshot, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        parser.add_argument("snapshotID", help="The ID of the VM")
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        snap = cli.get_snapshot(args.vmID, args.snapshotID)
        columns = ('Snapshot ID',
                   'VM ID',
                   'Disks')

        data = (
            snap["id"],
            snap["vm_id"],
            "\n".join(
                [d["name"] for d in snap["disks"]]
            )
        )
        return (columns, data)


class PurgeSnapshots(Command):

    def get_parser(self, prog_name):
        parser = super(PurgeSnapshots, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        cli.delete_all_snapshots(args.vmID)


class DeleteSnapshot(Command):

    def get_parser(self, prog_name):
        parser = super(DeleteSnapshot, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        parser.add_argument("snapshotID", help="The ID of the VM")
        return parser

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        cli.delete_snapshot(args.vmID, args.snapshotID)


class DownloadSnapshot(Command):

    def get_parser(self, prog_name):
        parser = super(DownloadSnapshot, self).get_parser(prog_name)
        parser.add_argument("vmID", help="The ID of the VM")
        parser.add_argument("snapshotID", help="The ID of the VM")
        parser.add_argument(
            "--out-dir",
            help="Destination folder for downloaded files.")
        parser.add_argument(
            "--diff-from",
            default=None,
            help=("Download only blocks that have changed from this"
                  " snapshot ID."))
        return parser

    def _create_or_expand_file(self, file_path, size):
        mode = "r+b"
        if os.path.isfile(file_path) is False:
            mode = "wb"
        with open(file_path, mode) as fd:
            # seek to end of file and get size.
            cur_size = fd.seek(0, 2)
            if cur_size > size:
                raise ValueError("cannot shrink disk")
            fd.truncate(size)

    def _download_disk(self, cli, args, disk):
        size = cli.get_disk_size(
            args.vmID, args.snapshotID, disk["name"])
        download_path = os.path.join(
            args.out_dir, disk["name"].lstrip("/"))
        self._create_or_expand_file(download_path, size)

        # read in chunks of 1 MB
        chunk_size = 1 * 1024 * 1024

        with open(download_path, "r+b") as fd:
            for chunk in disk["chunks"]:
                fd.seek(chunk["start"])
                with cli.download_chunk(
                    args.vmID, args.snapshotID,
                    disk["name"], chunk["start"],
                    chunk["length"], stream=True) as dl:

                    for data in dl.iter_content(chunk_size=chunk_size):
                        fd.write(data)

    def _ensure_out_dir(self, out_dir):
        if os.path.isdir(out_dir) is False:
            os.makedirs(out_dir)

    def take_action(self, args):
        cli = client.get_client_from_options(
            self._cmd_options)
        kw = {
            "compare_to": args.diff_from,
            "squash": True,
        }
        snap = cli.get_snapshot(
            args.vmID, args.snapshotID, **kw)
        self._ensure_out_dir(args.out_dir)

        for disk in snap["disks"]:
            self._download_disk(cli, args, disk)