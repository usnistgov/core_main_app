"""URL validation utils.

Used by callers that fetch a user/provider-configured URL server-side (e.g.
OAI-PMH harvesting) to guard against SSRF and credential-leak risks.
"""

import ipaddress
from urllib.parse import urlparse

from core_main_app import settings
from django.core.exceptions import ValidationError


def _get_origin(url: str) -> str | None:
    """
    Extract the scheme://netloc origin of a URL.

    Args:
        url: The URL string to parse.

    Returns:
        The origin string (e.g., 'https://example.com') if parsable, otherwise None.

    Example:
        >>> _get_origin("https://example.com/path?query=1")
        'https://example.com'
        >>> _get_origin("/relative/path")
        None
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return None
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_origin(url):
    """Is the given URL pointing back at this CDCS instance itself.

    Args:
        url:

    Returns:

    """
    url_origin = _get_origin(url)
    server_origin = _get_origin(settings.SERVER_URI)
    return url_origin is not None and url_origin == server_origin


def validate_request_url(url):
    """Validate a URL before it is fetched server-side.

    Deliberately narrow in scope and configurable via settings:
    - Rejects schemes not in settings.HTTP_ALLOWED_URL_SCHEMES, default http/https.
    - If settings.BLOCK_URL_LINK_LOCAL is True, rejects link-local addresses
      (e.g. 169.254.0.0/16, fe80::/10) which includes the cloud-metadata endpoint.
    - Rejects literal IPs listed in settings.BLOCKED_IP_LIST.

    Does NOT reject private/loopback IPs: self-harvesting
    e.g. http://localhost/... and internal-network federated harvesting
    between trusted instances are legitimate uses of this function's
    callers and must keep working.

    Does NOT resolve hostnames: a literal link-local IP in the URL is
    rejected, but a domain name that resolves to one is not caught here
    (DNS-rebinding is out of scope for this check).

    Args:
        url:

    Raises:
        ValidationError: if the URL uses a disallowed scheme, is a blocked IP, or
            link-local blocking is enabled and the host is link-local.

    """
    try:
        parsed_url = urlparse(url)
    except Exception as exc:
        raise ValidationError(
            f"URL '{url}' is not parsable: {str(exc)}"
        ) from exc

    if parsed_url.scheme not in settings.HTTP_ALLOWED_URL_SCHEMES:
        raise ValidationError(
            "URL scheme '%s' is not allowed." % parsed_url.scheme
        )

    try:
        host_ip = ipaddress.ip_address(parsed_url.hostname)
    except (ValueError, TypeError):
        return  # hostname is a domain name, not a literal IP
    except Exception as exc:
        raise ValidationError(
            f"An unexpected error occurred when parsing the URL hostname: {str(exc)}"
        ) from exc

    if settings.BLOCK_URL_LINK_LOCAL and host_ip.is_link_local:
        raise ValidationError(
            "URL host '%s' is a link-local address and is not allowed."
            % parsed_url.hostname
        )

    if str(host_ip) in settings.BLOCKED_IP_LIST:
        raise ValidationError(
            "URL host %s is amongst the blocked IP addresses."
            % parsed_url.hostname
        )
