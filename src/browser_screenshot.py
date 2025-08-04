from playwright.async_api import async_playwright, TimeoutError
from enum import Enum
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, TypedDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    # Mobile Phones - Increased scale for better quality
    DeviceType.IPHONE_13_PRO: {
        'width': 1170,  # 390 * 3
        'height': 2532,  # 844 * 3
        'is_mobile': True,
        'device_scale_factor': 3.0
    },
    DeviceType.SAMSUNG_GALAXY_S21: {
        'width': 360, 'height': 800, 'is_mobile': True, 'device_scale_factor': 3.0
    },
    # Tablets - Increased scale for better quality
    DeviceType.IPAD_AIR: {
        'width': 2360,  # 1180 * 2
        'height': 1640,  # 820 * 2
        'is_mobile': True,
        'device_scale_factor': 2.0
    },
    # Desktop - Increased resolution and scale for better quality
    DeviceType.DESKTOP: {
        'width': 2560,  # Higher base resolution
        'height': 1440,
        'is_mobile': False,
        'device_scale_factor': 2.0  # Increased from 1.0 to 2.0 for better quality
    }
}

class ScreenshotTaker:
    """Class to handle async screenshot capture with Playwright."""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()

    async def setup(self):
        """Initialize Playwright and browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-web-security']  # Disable CORS for local development
        )
        return self

    async def new_page(self):
        """Create a new browser context and page."""
        if not self.browser:
            await self.setup()
            
        self.context = await self.browser.new_context(
            viewport={
                'width': 1920,
                'height': 1080,
                'deviceScaleFactor': 2.0
            },
            device_scale_factor=2.0
        )
        self.page = await self.context.new_page()
        return self.page

    async def capture(
        self,
        url: str,
        output_path: str,
        device_type: str = DeviceType.DESKTOP,
        zoom_level: float = 1.0,
        quality: int = 100,  # Increased from 90 to 100 for maximum quality
        wait_for_load: bool = True,
        wait_after_load: int = 3000  # Added wait time after page load in ms
    ) -> str:
        """
        Capture a screenshot of the specified URL.
        
        Args:
            url: The URL to capture
            output_path: Where to save the screenshot
            device_type: Device type from DeviceType enum
            zoom_level: Zoom level for the page
            quality: Image quality (1-100)
            wait_for_load: Whether to wait for full page load
            
        Returns:
            Path to the saved screenshot
        """
        try:
            if not self.page:
                await self.new_page()

            device = DEVICE_PROFILES.get(device_type, DEVICE_PROFILES[DeviceType.DESKTOP])
            
            await self.page.set_viewport_size({
                'width': device['width'],
                'height': device['height'],
                'deviceScaleFactor': device['device_scale_factor']
            })

            logger.info(f"Navigating to {url}...")
            await self.page.goto(
                url,
                wait_until="networkidle" if wait_for_load else "domcontentloaded",
                timeout=self.timeout
            )
            
            if wait_for_load:
                await asyncio.sleep(2)  # Additional wait for dynamic content

            # Apply zoom if specified
            if zoom_level != 1.0:
                logger.info(f"Applying zoom level: {zoom_level}x")
                await self.page.evaluate(f"document.body.style.zoom = '{zoom_level}'")
                await asyncio.sleep(1)  # Wait for zoom to apply

            # Ensure directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Capturing high-quality screenshot to {output_path}...")
            # Additional wait to ensure all animations and transitions are complete
            await asyncio.sleep(wait_after_load / 1000)
            
            # Take screenshot with optimized settings
            screenshot_options = {
                'path': str(output_path),
                'full_page': True,
                'type': 'jpeg' if str(output_path).lower().endswith(('.jpg', '.jpeg')) else 'png',
                'quality': quality if str(output_path).lower().endswith(('.jpg', '.jpeg')) else None,
                'scale': 'device',  # Changed from 'css' to 'device' for higher quality
                'animations': 'disabled',  # Disable animations for cleaner capture
                'clip': None,
                'timeout': 30000  # 30 second timeout for large pages
            }
            
            # Take the screenshot
            await self.page.screenshot(**screenshot_options)
            
            logger.info("Screenshot saved successfully")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            raise

    async def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'context') and self.context:
            await self.context.close()
        if hasattr(self, 'browser') and self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright') and self.playwright:
            await self.playwright.stop()

# Helper function to maintain backward compatibility
async def capture_webpage(
    url: str,
    output_path: str,
    device_type: str = DeviceType.DESKTOP,
    zoom_level: float = 1.0,
    quality: int = 90,
    wait_for_load: bool = True
) -> str:
    """
    Helper function to maintain backward compatibility.
    Creates a new ScreenshotTaker instance for a single capture.
    """
    async with ScreenshotTaker() as st:
        return await st.capture(
            url=url,
            output_path=output_path,
            device_type=device_type,
            zoom_level=zoom_level,
            quality=quality,
            wait_for_load=wait_for_load
        )

# Example usage when run directly
if __name__ == "__main__":
    """
    Example usage of the capture_webpage function.
    Uncomment and modify the examples below to test different configurations.
    """
    
    # Example 1: Desktop screenshot with 2x zoom
    # capture_webpage(
    #     url="http://127.0.0.1:8000/",
    #     output_path="desktop_screenshot.jpg",
    #     device_type=DeviceType.DESKTOP,
    #     viewport_width=1920,
    #     viewport_height=1080,
    #     device_scale_factor=2.0,
    #     quality=95,
    #     zoom_level=2.0  # 2x zoom for higher quality
    # )
    
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
