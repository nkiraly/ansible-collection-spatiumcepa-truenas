from __future__ import absolute_import, division, print_function
from ansible_collections.spatiumcepa.truenas.plugins.module_utils.common import HTTPCode, HTTPResponse, \
    TruenasServerError, TruenasModelError, TruenasUnexpectedResponse, strip_null_module_params
from ansible_collections.spatiumcepa.truenas.plugins.module_utils.resources import TruenasSystemGeneral
from ansible_collections.spatiumcepa.truenas.plugins.module_utils.arg_specs import API_ARG_SPECS
from ansible.module_utils.connection import Connection, ConnectionError
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community"
}

DOCUMENTATION = """
module: truenas_api_system_general

short_description: Configure TrueNAS System General settings

description:
  - Configure TrueNAS System General settings via REST API

version_added: "0.1"

author: Nicholas Kiraly (@nkiraly)

options:
  model:
    type: dict
    description: ''
    options:
      crash_reporting:
        description: ''
        type: bool
      kbdmap:
        description: ''
        type: str
      language:
        description: ''
        type: str
      sysloglevel:
        choices:
        - F_EMERG
        - F_ALERT
        - F_CRIT
        - F_ERR
        - F_WARNING
        - F_NOTICE
        - F_INFO
        - F_DEBUG
        - F_IS_DEBUG
        description: ''
        type: str
      syslogserver:
        description: ''
        type: str
      timezone:
        description: ''
        type: str
      ui_address:
        description: ''
        type: list
      ui_certificate:
        description: ''
        type: int
      ui_httpsport:
        description: ''
        type: int
      ui_httpsprotocols:
        description: ''
        type: list
      ui_httpsredirect:
        description: ''
        type: bool
      ui_port:
        description: ''
        type: int
      ui_v6address:
        description: ''
        type: list
      usage_collection:
        description: ''
        type: bool
"""

EXAMPLES = """
  - name: System General Configuration via TrueNAS API
    spatiumcepa.truenas.truenas_api_system_general:
      model:
        ui_address: ['0.0.0.0']
        ui_httpsredirect: true
"""

RETURN = """
response:
  description: HTTP response returned from the API call
  returned: success
  type: dict
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            model=API_ARG_SPECS[TruenasSystemGeneral.RESOURCE_API_MODEL_SPEC]
        ),
        supports_check_mode=True,
    )

    connection = Connection(module._socket_path)
    system_general_resource = TruenasSystemGeneral(connection, module.check_mode)

    try:
        model_param = strip_null_module_params(module.params['model'])
        response = system_general_resource.update(model_param)
        module.exit_json(
            changed=system_general_resource.resource_changed,
            failed=response[HTTPResponse.STATUS_CODE] != HTTPCode.OK,
            response=response,
            submitted_model=model_param,
        )

    except TruenasServerError as e:
        module.fail_json(msg='Server returned an error, satus code: %s. '
                             'Server response: %s' % (e.code, e.response))

    except TruenasModelError as e:
        module.fail_json(msg='Data model error: %s' % (e.args[0]))

    except TruenasUnexpectedResponse as e:
        module.fail_json(msg=e.args[0])

    except ConnectionError as e:
        module.fail_json(msg=e.args[0])


if __name__ == '__main__':
    main()
