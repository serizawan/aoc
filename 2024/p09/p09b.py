class DiskBlock:
    def __init__(self, is_empty, i, j, fid=None):
        self.is_empty = is_empty
        self.i = i
        self.j = j
        self.fid = fid

    @property
    def length(self):
        return self.j - self.i

    def __repr__(self):
        return f"{self.is_empty=}, {self.i=}, {self.j=}, {self.fid=}"

if __name__ == "__main__":
    disk_map_dense = open(0).read()
    disk_files =[]
    disk_frees = []
    is_free = False
    end_of_disk_i = 0
    for i, l in enumerate(disk_map_dense):
        if is_free:
            disk_frees.append(DiskBlock(is_free, end_of_disk_i, end_of_disk_i + int(l)))
        else:
            disk_files.append(DiskBlock(is_free, end_of_disk_i, end_of_disk_i + int(l), str(i // 2)))
        end_of_disk_i += int(l)
        is_free = not is_free

    for disk_file in disk_files[::-1]:
        for disk_free in disk_frees:
            if disk_file.length <= disk_free.length and disk_free.i < disk_file.i:
                disk_file.i, disk_file.j = disk_free.i, disk_free.i + disk_file.length
                disk_free.i += disk_file.length
                break

    checksum = 0
    for disk_file in disk_files:
        for k in range(disk_file.i, disk_file.j):
            checksum += k * int(disk_file.fid)

    print(checksum)