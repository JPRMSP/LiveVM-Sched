import streamlit as st
import random
import time

st.set_page_config(page_title="LiveVM-Sched", layout="wide")
st.title("🖥️ LiveVM-Sched: VM & Resource Scheduling Simulator")

# ===================== DISK SCHEDULING =====================
st.header("💽 Disk Scheduling (UNIT I)")

disk_algo = st.selectbox("Disk Scheduling Algorithm", ["FCFS", "SSTF"])
disk_requests = random.sample(range(0, 200), 8)
head = random.randint(0, 199)

def fcfs(req, head):
    seek = 0
    pos = head
    for r in req:
        seek += abs(pos - r)
        pos = r
    return seek, req

def sstf(req, head):
    req = req[:]
    seek = 0
    pos = head
    order = []
    while req:
        nearest = min(req, key=lambda x: abs(x - pos))
        seek += abs(pos - nearest)
        pos = nearest
        order.append(nearest)
        req.remove(nearest)
    return seek, order

if disk_algo == "FCFS":
    seek, order = fcfs(disk_requests, head)
else:
    seek, order = sstf(disk_requests, head)

st.write("**Initial Head Position:**", head)
st.write("**Request Queue:**", disk_requests)
st.write("**Seek Order:**", order)
st.success(f"Total Seek Time: {seek}")

st.divider()

# ===================== GRID + VM SCHEDULING =====================
st.header("🌐 Virtualized Grid Scheduling (UNIT II & III)")

class VM:
    def __init__(self, vid, cpu):
        self.vid = vid
        self.cpu = cpu

class Host:
    def __init__(self, hid):
        self.hid = hid
        self.capacity = 100
        self.used = 0
        self.vms = []

    def allocate(self, vm):
        if self.used + vm.cpu <= self.capacity:
            self.vms.append(vm)
            self.used += vm.cpu
            return True
        return False

clusters = {
    "Grid Site A": [Host("A-Host1"), Host("A-Host2")],
    "Grid Site B": [Host("B-Host1"), Host("B-Host2")]
}

vms = [VM(f"VM{i+1}", random.randint(15, 40)) for i in range(6)]

for vm in vms:
    for site in clusters.values():
        allocated = False
        for host in site:
            if host.allocate(vm):
                allocated = True
                break
        if allocated:
            break

cols = st.columns(2)
for i, (site, hosts) in enumerate(clusters.items()):
    with cols[i]:
        st.subheader(site)
        for h in hosts:
            st.metric(h.hid, f"{h.used}/100 CPU", f"{len(h.vms)} VMs")
            for vm in h.vms:
                st.write(f"• {vm.vid} ({vm.cpu} CPU)")

st.divider()

# ===================== LIVE VM MIGRATION =====================
st.header("🔁 Live VM Migration (VMware vMotion Concept)")

if st.button("Trigger Live Migration"):
    src = clusters["Grid Site A"][0]
    dst = clusters["Grid Site B"][0]

    if src.vms:
        vm = src.vms.pop()
        src.used -= vm.cpu

        progress = st.progress(0)
        status = st.empty()

        for i in range(100):
            progress.progress(i + 1)
            status.info(f"Migrating {vm.vid}... {i+1}%")
            time.sleep(0.02)

        dst.vms.append(vm)
        dst.used += vm.cpu
        status.success(f"Migration Complete: {vm.vid} → {dst.hid}")

st.divider()
