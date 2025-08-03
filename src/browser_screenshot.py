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

class DeviceConfig(TypedDict):
    """Configuration for a device profile."""
    width: int
    height: int
    is_mobile: bool
    device_scale_factor: float


def capture_webpage(
    url: str,
    output_path: str = "screenshot.png",
    viewport_width: Optional[int] = None,
    viewport_height: Optional[int] = None,
    device_scale_factor: float = 2.0,
    quality: int = 90,
    device_type: Literal['mobile', 'tablet', 'desktop'] = 'desktop',
    device_name: Optional[str] = None,
    full_page: bool = True,
    wait_for_load: bool = True
) -> None:
    """
    Capture a high-quality screenshot of a webpage using Playwright.

    Args:
        url: The URL of the webpage to capture
        output_path: Path to save the screenshot file (default: "screenshot.png")
        viewport_width: Viewport width in pixels (overrides device preset)
        viewport_height: Viewport height in pixels (overrides device preset)
        device_scale_factor: Pixel ratio for high-DPI screens (default: 2.0)
        quality: Image quality (1-100) for JPEG format (default: 90)
        device_type: General device category (default: 'desktop')
        device_name: Specific device profile to use
        full_page: Whether to capture the entire scrollable page (default: True)
        wait_for_load: Wait for network to be idle before capturing (default: True)
    """
    # Device profiles database
    DEVICE_PROFILES: Dict[str, DeviceConfig] = {
        # Mobile Phones - High-end
        'iphone_13_pro': {
            'width': 390, 'height': 844, 'is_mobile': True, 'device_scale_factor': 3.0
        },
        'samsung_galaxy_s21': {
            'width': 360, 'height': 800, 'is_mobile': True, 'device_scale_factor': 3.0
        },
        'pixel_5': {
            'width': 393, 'height': 851, 'is_mobile': True, 'device_scale_factor': 2.75
        },
        'iphone_se': {
            'width': 375, 'height': 667, 'is_mobile': True, 'device_scale_factor': 2.0
        },
        
        # Tablets
        'ipad_air': {
            'width': 1180, 'height': 820, 'is_mobile': True, 'device_scale_factor': 2.0
        },
        'samsung_galaxy_tab_s7': {
            'width': 800, 'height': 1280, 'is_mobile': True, 'device_scale_factor': 2.0
        },
        
        # Desktop (default)
        'desktop': {
            'width': viewport_width or 1920,
            'height': viewport_height or 1080,
            'is_mobile': False,
            'device_scale_factor': device_scale_factor
        }
    }

    # Select device profile
    profile = DEVICE_PROFILES.get(device_name or device_type, DEVICE_PROFILES['desktop']).copy()
    
    # Override dimensions if explicitly provided
    if viewport_width:
        profile['width'] = viewport_width
    if viewport_height:
        profile['height'] = viewport_height
    
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
            
            print(f"Capturing screenshot to {output_path}...")
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
    
    # Example 1: Desktop screenshot
    # capture_webpage(
    #     url="https://example.com",
    #     output_path="desktop_screenshot.jpg",
    #     viewport_width=1920,
    #     viewport_height=1080,
    #     device_scale_factor=2.0,
    #     quality=95
    # )
    
    # Example 2: Mobile device screenshot
    # capture_webpage(
    #     url="https://example.com/mobile",
    #     output_path="mobile_screenshot.jpg",
    #     device_name='iphone_13_pro',
    #     quality=95
    # )
    
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
