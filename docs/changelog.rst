=========
Changelog
=========

----------------
Version 0 (Beta)
----------------

0.9.1 (2020-Apr-25)
===================

Bug Fixes
---------

* Marking the ``helcim_js.identifier.test_input`` as a Django ``SafeString``,
  to allow usage without manual escpaing in templates.

0.9.0 (2020-Apr-23)
===================

Feature Updates
---------------

* Adding new settings key under the ``HELCIM_JS_CONFIG`` setting.
  Can now include ``test: True`` for each Helcim.js configuration.
  When enabled, you can use ``helcim_js.identifier.test_input`` to
  enable or disable test mode within the Django template.

0.8.1 (2020-Apr-23)
===================

Bug Fixes
---------

* Fixing bug with the Helcim token "First 4 Last 4" characters saving;
  Helcim.js response may include whitespace in credit card number,
  so this needs to be stripped out.

0.8.0 (2020-Apr-21)
===================

Feature Updates
---------------

* Switching the ``HELCIM_ASSOCIATE_USER`` setting to
  ``HELCIM_ALLOW_ANONYMOUS``. This will allow clearer support for
  anonymous transactions.
* Adding support for Helcim.js.

  * Provides new ``gateway`` class which can be used to manage
    Helcim.js responses, perform data conversion into Python data
    types, complete validations, complete redactions, and save details
    to the ``HelcimTransaction`` and ``HelcimToken`` models.
  * Updates allowable settings to allow declaration of a
    ``HELCIM_JS_CONFIG`` setting. This setting will allow declaration
    of Helcim.js configuration details within the Django settings.
  * Provides new mixin for Django Views. Updates view context to
    include the ``HELCIM_JS_CONFIG`` details, allowing streamlined
    declaration of configuration details in Django templates.

* ``django-helcim`` will no longer require specifying Helcim API
  details in the settings, as either the API or Helcim.js workflow
  can be used with the package.
* Adding a new sandbox site that shows how Django Helcim can be
  integrated into a project from scratch. This site demonstrates
  both the Helcim API workflow and the Helcim.js workflow.
* Docs updated with new details on integrating ``django-helcim`` with
  a Django project.

Bug Fixes
---------

* Add verify/verification (``v``) as an allowable transaction type for
  the ``HelcimTransaction`` model. Other calls in package were
  expecting this type.

0.7.1 (2020-Apr-05)
===================

Bug Fixes
---------

* Fixed issue with ``__str__`` of transaction model in Django admin
  when timezones were used for ``datetimes``.

0.7.0 (2019-Dec-15)
===================

Feature Updates
---------------

* Removing official support for Django 2.1 (has reached end of life).
* Removing Tox from testing. Too many conflicting issues and CI system
  can handle this better now.

0.6.0 (2019-Nov-17)
===================

Feature Updates
---------------

* Adding a Django user reference to the ``HelcimTransaction`` model.
* Reworking the settings around associating a user model to the
  django-helcim models. Now all settings are controlled by the
  ``HELCIM_ASSOCIATE_USER`` setting.

0.5.0 (2019-Nov-16)
===================

Feature Updates
---------------

* Adding cardholder name and CC expiry to token model and saving
  details with token.
* Updating related_name of token model to reduce naming conflicts.

0.4.0 (2019-Sep-07)
===================

Feature Updates
---------------

* Updating the Oscar components for Oscar 2.0 compatibility.
* Sandbox updated to accomodate Oscar changes.

0.3.1 (2018-Nov-25)
===================

Bug Fixes
---------

* Fixed bug where Helcim Commerce API may return a blank response
  for a string field, resulting in coercion of ``None`` to ``'None'``.

0.3.0 (2018-Nov-24)
===================

Feature Updates
---------------

* Added new functions to ``gateway`` module to:

  * retrieve a user's saved Helcim tokens;
  * retrieve details of a single Helcim token; and
  * manage settings (this will verify that any required settings
    declared and will provide defaults for all other settings as
    appropriate).

* Extended the ``bridge_oscar`` module to:

  * streamline validating a Helcim token for payment processing by
    Django Oscar;
  * handle whether a token should be associated with a ``django_user``
    instance or a Helcim ``customer_code``; and
  * provide convenience shortcut functions/dictionaries to
    the ``bridge_oscar`` module to access functionality in
    the ``gateway`` module.

* Updated the ``TO_API`` dictionary to remove ``order_number`` (not
  recognized by the Helcim Commerce API).
* Updated sandbox site to demonstrate a workflow that makes use of the
  Token Vault.
* Updated HelcimToken model to:

  * record credit card type;
  * display the "first 4 last 4" digits of the credit card number as a
    16 character string; and
  * retrieve and display an image for the corresponding credit card
    type.

Bug Fixes
---------

* Fixed the ``refund`` and ``capture`` views to make use of the proper
  settings (were still using the
  outdated ``HELCIM_TRANSACTIONS_READ_ONLY`` setting).

0.2.2 (2018-Nov-17)
===================

Bug Fixes
---------

* Removing unnecessary ``app_name`` from urls which may cause namespace
  issues.

0.2.1 (2018-Nov-17)
===================

Bug Fixes
---------

* HTML template files are now included in package when installed via
  PyPI.

0.2.0 (2018-Nov-14)
===================

Feature Updates
---------------

* Added the HelcimToken model (AKA the "Token Vault") - allows saving of
  Helcim Commerce card tokens to allow re-use in later transactions.
* Made functions for HelcimTransaction views more configurable - can
  now choose exactly which features to enable and disable.
* Reworked settings to default to more conservative values. Thinks will
  generally be disabled or redacted by default, but can be enabled as
  needed.
* Added redaction settings for credit card CVV, credit card magnetic
  strip data, and encrypted credit card magnetic strip data.
* Improved sandbox functioning to make setting up a new demo site
  easier.

Bug Fixes
---------

* Fixed issues where the ``HELCIM_REDACT_ALL`` flag was not overriding
  properly.
* Updated redaction functions to accommodate  all known fields
  containing cardholder information.
* Fixed issue where POST requests were returning byte-data rather than
  string data.

0.1.2 (2018-Nov-08)
===================

Feature Updates
---------------

* Adding DepreciationWarning for Django 1.11 in anticipation of eventual end
  of support in 2020.
* Adding Tox test environments for all combinations of supported Python
  and Django versions.

0.1.1 (2018-Nov-07)
===================

Bug Fixes
---------

* Properly specifying dependencies for PyPI installation and updating
  Pipfile.

0.1.0 (2018-Nov-03)
===================

Feature Updates
---------------

* Initial package release
* Supports basic API functions: purchase (sale), pre-authorization, capture,
  refund
* Basic ``django-oscar`` support with the bridge module.
