"""Common types and enums for Novita API models."""

from enum import Enum


class ModelName(str, Enum):
    """Commonly used model names."""

    # Stable Diffusion models
    SD_XL_BASE = "sd_xl_base_1.0.safetensors"
    SD_XL_TURBO = "sdxlTurbo_v1.safetensors"
    SD_15 = "sd_v1-5.safetensors"
    SD_21 = "sd_2-1.safetensors"
    DREAMSHAPER = "dreamshaper_8.safetensors"
    REALISTIC_VISION = "realisticVisionV60B1_v51VAE.safetensors"


class Sampler(str, Enum):
    """Available sampling methods."""

    EULER = "Euler"
    EULER_A = "Euler a"
    DPM_PLUS_PLUS_2M = "DPM++ 2M"
    DPM_PLUS_PLUS_2M_KARRAS = "DPM++ 2M Karras"
    DPM_PLUS_PLUS_SDE = "DPM++ SDE"
    DPM_PLUS_PLUS_SDE_KARRAS = "DPM++ SDE Karras"
    HEUN = "Heun"
    LMS = "LMS"
    LMS_KARRAS = "LMS Karras"
    DDIM = "DDIM"
    PLMS = "PLMS"


class ResponseFormat(str, Enum):
    """Response format for generated images."""

    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"


class InstanceType(str, Enum):
    """GPU instance types for cloud deployment."""

    A100_80GB = "A100_80GB"
    A100_40GB = "A100_40GB"
    A10 = "A10"
    L40 = "L40"
    RTX_4090 = "RTX_4090"
    RTX_A6000 = "RTX_A6000"


class EndpointStatus(str, Enum):
    """Status of a deployed endpoint."""

    PENDING = "PENDING"
    CREATING = "CREATING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    TERMINATING = "TERMINATING"
