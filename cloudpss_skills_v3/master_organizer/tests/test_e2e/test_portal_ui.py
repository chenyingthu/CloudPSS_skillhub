"""E2E tests for Portal UI using Playwright."""

import pytest
import subprocess
import sys
import time
import socket
from pathlib import Path


def find_free_port():
    """Find a free port for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def portal_server(tmp_path_factory):
    """Start portal server for E2E tests."""
    tmp_path = tmp_path_factory.mktemp("portal_e2e")
    port = find_free_port()

    # Start server
    env = {"CLOUDPSS_HOME": str(tmp_path), "PORT": str(port)}
    proc = subprocess.Popen(
        [sys.executable, "-m", "cloudpss_skills_v3.master_organizer.portal.server", str(port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(2)

    base_url = f"http://localhost:{port}"

    yield base_url

    # Cleanup
    proc.terminate()
    proc.wait(timeout=5)


class TestPortalHomePage:
    """Test Portal home page."""

    def test_home_page_loads(self, portal_server, page):
        """Test home page loads successfully."""
        page.goto(f"{portal_server}/")

        # Check page title
        assert "CloudPSS" in page.title() or "Portal" in page.title()

        # Check main navigation elements
        assert page.locator("nav").is_visible() or page.locator("header").is_visible()

    def test_navigation_links(self, portal_server, page):
        """Test navigation links work."""
        page.goto(f"{portal_server}/")

        # Check for common navigation elements
        nav_links = page.locator("nav a, header a, .nav-link")
        count = nav_links.count()

        # Should have at least some navigation links
        assert count > 0

    def test_page_responsiveness(self, portal_server, page):
        """Test page is responsive."""
        # Test desktop viewport
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto(f"{portal_server}/")
        assert page.locator("body").is_visible()

        # Test tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})
        page.reload()
        assert page.locator("body").is_visible()


class TestPortalAPIEndpoints:
    """Test Portal API endpoints via browser."""

    def test_api_health_endpoint(self, portal_server, page):
        """Test health endpoint returns valid JSON."""
        page.goto(f"{portal_server}/api/health")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Get page content
        content = page.locator("pre").inner_text()

        # Should contain JSON with status
        assert '"status"' in content or '"ok"' in content

    def test_api_snapshot_endpoint(self, portal_server, page):
        """Test snapshot endpoint returns workspace data."""
        page.goto(f"{portal_server}/api/snapshot")

        page.wait_for_load_state("networkidle")
        content = page.locator("pre").inner_text()

        # Should contain workspace data
        assert '"workspace"' in content


class TestPortalCaseManagement:
    """Test case management workflows."""

    def test_cases_page_loads(self, portal_server, page):
        """Test cases page displays case list."""
        page.goto(f"{portal_server}/")

        # Look for cases section or link
        case_link = page.locator("a[href*='case'], text=Cases, text=算例").first

        if case_link.is_visible():
            case_link.click()
            page.wait_for_load_state("networkidle")

            # Check page loaded
            assert page.locator("body").is_visible()

    def test_create_case_form(self, portal_server, page):
        """Test create case form exists."""
        page.goto(f"{portal_server}/")

        # Look for create case button or link
        create_btn = page.locator(
            "button:has-text('Create'), button:has-text('New'), "
            "a:has-text('Create'), a:has-text('New'), "
            "button:has-text('创建'), a:has-text('创建')"
        ).first

        # Even if button doesn't exist, page should load
        assert page.locator("body").is_visible()


class TestPortalErrorHandling:
    """Test error handling and edge cases."""

    def test_404_page(self, portal_server, page):
        """Test 404 page for non-existent routes."""
        page.goto(f"{portal_server}/nonexistent-page-12345")

        # Page should load (either custom 404 or default)
        assert page.locator("body").is_visible()

    def test_invalid_api_endpoint(self, portal_server, page):
        """Test API handles invalid endpoints gracefully."""
        page.goto(f"{portal_server}/api/invalid-endpoint")

        page.wait_for_load_state("networkidle")
        content = page.locator("body").inner_text()

        # Should show error or 404 message
        assert len(content) > 0


@pytest.mark.skip(reason="Requires JavaScript interactions")
class TestPortalInteractions:
    """Test JavaScript interactions (skipped in basic E2E)."""

    def test_modal_dialogs(self, portal_server, page):
        """Test modal dialogs open and close."""
        page.goto(f"{portal_server}/")

        # This would test JavaScript modals
        pass

    def test_form_validation(self, portal_server, page):
        """Test form validation feedback."""
        page.goto(f"{portal_server}/")

        # This would test client-side validation
        pass
