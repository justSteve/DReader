"""Channel registry — reads discord-config.yaml for target management."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]


@dataclass
class ChannelTarget:
    channel_id: str
    channel_name: str
    server_id: str
    server_name: str

    @property
    def url(self) -> str:
        return f"https://discord.com/channels/{self.server_id}/{self.channel_id}"


@dataclass
class Registry:
    targets: list[ChannelTarget] = field(default_factory=list)
    scraping: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: str = "discord-config.yaml") -> Registry:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        data = yaml.safe_load(path.read_text())
        targets: list[ChannelTarget] = []
        for server in data.get("servers", []):
            for channel in server.get("channels", []):
                targets.append(
                    ChannelTarget(
                        channel_id=channel["id"],
                        channel_name=channel["name"],
                        server_id=server["id"],
                        server_name=server["name"],
                    )
                )
        return cls(targets=targets, scraping=data.get("scraping", {}))

    def find(self, query: str) -> list[ChannelTarget]:
        """Find targets by channel ID, name substring, or server ID."""
        q = query.lower()
        return [
            t for t in self.targets
            if q in t.channel_id
            or q in t.channel_name.lower()
            or q in t.server_id
            or q in t.server_name.lower()
        ]

    def by_server(self, server_id: str) -> list[ChannelTarget]:
        return [t for t in self.targets if t.server_id == server_id]

    @property
    def server_ids(self) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for t in self.targets:
            if t.server_id not in seen:
                seen.add(t.server_id)
                result.append(t.server_id)
        return result
