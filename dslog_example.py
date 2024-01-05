import re
from dslogs.dslogstream import DsLogStream
from dslogs.dseventstream import DsEventStream
from dataclasses import dataclass
import pandas as pd
from matplotlib import pyplot as plt


@dataclass
class MatchData:
    battery_code: str
    data: pd.DataFrame


SEARCH_PATTERN = f"Battery code: (.*)"


def load_battery_code(filename: str) -> str:
    with open(filename + ".dsevents", "rb") as file:
        for entry in DsEventStream(file):
            message = entry.message.get("message")
            if not message:
                continue
            if match := re.search(SEARCH_PATTERN, message):
                code = match.group(1)
                return code
    return ""


def load_power_data(filename: str) -> pd.DataFrame:
    log_data = {
        "date": [],
        "voltage": [],
        "pdp_voltage": [],
        "pdp_current": [],
    }

    with open(filename + ".dslog", "rb") as file:
        for entry in DsLogStream(file):
            log_data["date"].append(entry.date)
            log_data["voltage"].append(entry.voltage)
            log_data["pdp_voltage"].append(entry.pdp_data.voltage)
            log_data[f"pdp_current"] = sum(entry.pdp_data.currents)
    df = pd.DataFrame(log_data)
    df["timestamp"] = df["date"].astype(int)
    df["timestamp"] = df["timestamp"].div(1e9)
    df["timestamp"] = df["timestamp"].sub(df["timestamp"].iloc[0])
    return df


def main() -> None:
    filename = "data/2024_01_04 20_48_11 Thu"
    battery_log = MatchData(battery_code="", data=pd.DataFrame())
    battery_log.battery_code = load_battery_code(filename)
    battery_log.data = load_power_data(filename)

    plt.title(f"Battery {battery_log.battery_code} performance over time")
    plt.plot(
        battery_log.data["timestamp"], battery_log.data["voltage"], label="Voltage"
    )
    plt.ylim(0, 13)
    plt.show()


if __name__ == "__main__":
    main()
