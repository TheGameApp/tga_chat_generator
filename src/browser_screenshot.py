"""
Webpage screenshot capture utility using Playwright.

This module provides functionality to capture screenshots of web pages with
support for various devices, viewport sizes, and quality settings.

Example usage:
    from browser_screenshot import capture_webpage
    
    # Basic usage
    capture_webpage(
        url="https://example.com",
        output_path="screenshot.png"
    )
    
    # With custom device settings
    capture_webpage(
        url="https://example.com",
        output_path="mobile.png",
        device_name='iphone_13_pro'
    )
"""

from playwright.sync_api import sync_playwright
from typing import Optional, Literal, Dict, Any, TypedDict
from enum import Enum

class DeviceType(str, Enum):
    """Supported device types for screenshots."""
    IPHONE_13_PRO = "iphone_13_pro"
    SAMSUNG_GALAXY_S21 = "samsung_galaxy_s21"
    PIXEL_5 = "pixel_5"
    IPHONE_SE = "iphone_se"
    IPAD_AIR = "ipad_air"
    SAMSUNG_GALAXY_TAB_S7 = "samsung_galaxy_tab_s7"
    DESKTOP = "desktop"

class DeviceConfig(TypedDict):
    """Configuration for a device profile."""
    width: int
    height: int
    is_mobile: bool
    device_scale_factor: float

# Device profiles database
DEVICE_PROFILES: Dict[str, DeviceConfig] = {
    # Mobile Phones
    DeviceType.IPHONE_13_PRO: {
        'width': 390, 'height': 844, 'is_mobile': True, 'device_scale_factor': 3.0
    },
    DeviceType.SAMSUNG_GALAXY_S21: {
        'width': 360, 'height': 800, 'is_mobile': True, 'device_scale_factor': 3.0
    },
    # Tablets
    DeviceType.IPAD_AIR: {
        'width': 1180, 'height': 820, 'is_mobile': True, 'device_scale_factor': 2.0
    },
    # Desktop (default)
    DeviceType.DESKTOP: {
        'width': 1920, 'height': 1080, 'is_mobile': False, 'device_scale_factor': 1.0
    }
}


def capture_webpage(
    url: str,
    output_path: str = "screenshot.png",
    viewport_width: Optional[int] = None,
    viewport_height: Optional[int] = None,
    device_scale_factor: float = 2.0,
    quality: int = 90,
    device_type: str = DeviceType.DESKTOP,
    full_page: bool = True,
    wait_for_load: bool = True,
    zoom_level: float = 1.0
) -> None:
    """
    Capture a high-quality screenshot of a webpage using Playwright.

    Args:
        url: URL of the webpage to capture
        output_path: Path to save the screenshot (default: 'screenshot.png')
        viewport_width: Viewport width in pixels (overrides device default)
        viewport_height: Viewport height in pixels (overrides device default)
        device_scale_factor: Device scale factor (default: 2.0 for high DPI)
        quality: Image quality (1-100) for JPEG (default: 90)
        device_type: Device type from DeviceType enum (default: DESKTOP)
        full_page: Whether to capture the entire scrollable page (default: True)
        wait_for_load: Wait for network to be idle before capturing (default: True)
        zoom_level: Zoom level for the screenshot (default: 1.0)
    """
    # Select device profile and create a copy to modify
    profile = DEVICE_PROFILES.get(DeviceType(device_type), DEVICE_PROFILES[DeviceType.DESKTOP]).copy()
    
    # Update device scale factor if provided
    if device_scale_factor:
        profile['device_scale_factor'] = device_scale_factor
    
    # Set higher resolution for better quality
    quality_multiplier = 2  # Double the resolution for better quality
    
    # Override dimensions if explicitly provided, otherwise use device profile with quality multiplier
    if viewport_width:
        profile['width'] = viewport_width
    else:
        profile['width'] *= quality_multiplier
        
    if viewport_height:
        profile['height'] = viewport_height
    else:
        profile['height'] *= quality_multiplier
    
    # Increase device scale factor for better quality
    profile['device_scale_factor'] = 2.0
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        
        try:
            context = browser.new_context(
                viewport={
                    'width': profile['width'],
                    'height': profile['height']
                },
                device_scale_factor=profile['device_scale_factor'],
                is_mobile=profile['is_mobile'],
                has_touch=profile['is_mobile'],
                ignore_https_errors=True,
                user_agent=(
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 '
                    '(KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
                    if profile['is_mobile'] else None
                )
            )
            
            page = context.new_page()
            page.set_default_timeout(60000)  # 60 second timeout
            
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="networkidle" if wait_for_load else "domcontentloaded")
            
            if wait_for_load:
                page.wait_for_timeout(2000)  # Additional wait for dynamic content
            
            # Apply zoom if specified
            if zoom_level != 1.0:
                print(f"Applying zoom level: {zoom_level}x")
                page.evaluate(f"document.body.style.zoom = '{zoom_level}'")
            
            # Wait for any potential zoom-related rendering
            page.wait_for_timeout(1000)
            
            print(f"Capturing high-quality screenshot to {output_path}...")
            page.screenshot(
                path=output_path,
                full_page=full_page,
                type='jpeg' if output_path.lower().endswith(('.jpg', '.jpeg')) else 'png',
                quality=quality if output_path.lower().endswith(('.jpg', '.jpeg')) else None,
                scale='css'
            )
            print("Screenshot saved successfully")
            
        except Exception as error:
            print(f"Error capturing screenshot: {error}")
            raise
            
        finally:
            browser.close()

# Example usage when run directly
if __name__ == "__main__":
    """
    Example usage of the capture_webpage function.
    Uncomment and modify the examples below to test different configurations.
    """
    
    # Example 1: Desktop screenshot with 2x zoom
    capture_webpage(
        url="http://127.0.0.1:8000/",
        output_path="desktop_screenshot.jpg",
        device_type=DeviceType.DESKTOP,
        viewport_width=1920,
        viewport_height=1080,
        device_scale_factor=2.0,
        quality=95,
        zoom_level=2.0  # 2x zoom for higher quality
    )
    
    # Example 2: Mobile device screenshot with 2x zoom
    capture_webpage(
        url="http://127.0.0.1:8000/",
        output_path="mobile_screenshot.jpg",
        device_type=DeviceType.IPHONE_13_PRO,
        quality=95,
        zoom_level=2.0
    )
    
    # Example 3: Custom viewport with high quality
    # capture_webpage(
    #     url="https://example.com/custom",
    #     output_path="custom_screenshot.jpg",
    #     viewport_width=1440,
    #     viewport_height=900,
    #     device_scale_factor=2.0,
    #     quality=100,
    #     full_page=True
    # )
    
    print("Please uncomment and modify the example code to run specific tests.")
    print("For more information, see the module docstring or README.md")
