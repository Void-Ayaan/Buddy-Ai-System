import psutil

def analyze_disk_storage():
    """Analyze all mounted storage drives and report free gigabytes and percentage."""
    try:
        partitions = psutil.disk_partitions(all=False)
        reports = []

        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                total_gb = round(usage.total / (1024**3), 1)
                free_gb = round(usage.free / (1024**3), 1)
                used_pct = usage.percent
                reports.append(f"Drive {p.mountpoint[:2]}: {free_gb} GB free of {total_gb} GB ({used_pct}% used)")
            except Exception:
                continue

        if reports:
            summary = " | ".join(reports)
            return f"Storage Breakdown, Boss: {summary}."
        else:
            return "Could not retrieve storage breakdown, Boss."
    except Exception as e:
        return f"Disk storage analysis error: {e}"
