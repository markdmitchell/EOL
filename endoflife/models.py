from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ProductVersion:
    name: str
    date: Optional[str] = None
    link: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductVersion":
        if not data:
            return None
        return cls(
            name=data.get("name", ""),
            date=data.get("date"),
            link=data.get("link"),
        )

@dataclass
class ReleaseCycle:
    name: str
    release_date: Optional[str] = None
    is_eol: bool = False
    eol_from: Optional[str] = None
    is_lts: bool = False
    lts_from: Optional[str] = None
    is_eoas: Optional[bool] = None
    eoas_from: Optional[str] = None
    is_discontinued: Optional[bool] = None
    discontinued_from: Optional[str] = None
    is_eoes: Optional[bool] = None
    eoes_from: Optional[str] = None
    is_maintained: bool = False
    codename: Optional[str] = None
    label: Optional[str] = None
    latest: Optional[ProductVersion] = None
    custom: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReleaseCycle":
        latest_data = data.get("latest")
        latest_obj = ProductVersion.from_dict(latest_data) if latest_data and isinstance(latest_data, dict) else None
        
        # Handle string or boolean for eol / lts / eoas fields if present
        eol_val = data.get("isEol", False)
        if isinstance(eol_val, str):
            eol_val = eol_val.lower() == "true"

        return cls(
            name=str(data.get("name", "")),
            release_date=data.get("releaseDate"),
            is_eol=bool(eol_val),
            eol_from=data.get("eolFrom"),
            is_lts=bool(data.get("isLts", False)),
            lts_from=data.get("ltsFrom"),
            is_eoas=data.get("isEoas"),
            eoas_from=data.get("eoasFrom"),
            is_discontinued=data.get("isDiscontinued"),
            discontinued_from=data.get("discontinuedFrom"),
            is_eoes=data.get("isEoes"),
            eoes_from=data.get("eoesFrom"),
            is_maintained=bool(data.get("isMaintained", False)),
            codename=data.get("codename"),
            label=data.get("label"),
            latest=latest_obj,
            custom=data.get("custom"),
        )

@dataclass
class ProductSummary:
    name: str
    label: str
    aliases: List[str] = field(default_factory=list)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    uri: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductSummary":
        return cls(
            name=data.get("name", ""),
            label=data.get("label", data.get("name", "")),
            aliases=data.get("aliases", []),
            category=data.get("category"),
            tags=data.get("tags", []),
            uri=data.get("uri"),
        )

@dataclass
class ProductDetails:
    name: str
    label: str
    aliases: List[str] = field(default_factory=list)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    version_command: Optional[str] = None
    identifiers: List[Dict[str, Any]] = field(default_factory=list)
    releases: List[ReleaseCycle] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductDetails":
        raw_releases = data.get("releases", [])
        releases = [ReleaseCycle.from_dict(r) for r in raw_releases if isinstance(r, dict)]
        return cls(
            name=data.get("name", ""),
            label=data.get("label", data.get("name", "")),
            aliases=data.get("aliases", []),
            category=data.get("category"),
            tags=data.get("tags", []),
            version_command=data.get("versionCommand"),
            identifiers=data.get("identifiers", []),
            releases=releases,
        )

@dataclass
class ResourceLink:
    name: str
    uri: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResourceLink":
        return cls(
            name=data.get("name", ""),
            uri=data.get("uri", "")
        )
