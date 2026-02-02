# 快速修复 - 简化版本（每个 Board 最多 250 个 Pin）

---

**Blueprint ID**: `N/A`
**Name**: The Quick Fix – Simple Version (Limited to 250 pins / board)
**Description**: N/A
**Version**: N/A

## Metadata / 元数据

- **instant**: False
- **version**: 1
- **scenario**: {'roundtrips': 1, 'maxErrors': 3, 'autoCommit': True, 'autoCommitTriggerLast': True, 'sequential': False, 'slots': None, 'confidential': False, 'dataloss': False, 'dlq': False, 'freshVariables': False}
- **designer**: {'orphans': []}
- **zone**: us2.make.com
- **notes**: []

## Raw JSON (for reference) / 原始 JSON（供参考）

```json
{
  "name": "The Quick Fix \u2013 Simple Version (Limited to 250 pins / board)",
  "flow": [
    {
      "id": 14,
      "module": "pinterest:listBoards",
      "version": 2,
      "parameters": {
        "__IMTCONN__": 1368953
      },
      "mapper": {
        "limit": "150"
      },
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0
        },
        "restore": {
          "expect": {
            "ad_account_id": {
              "mode": "chose"
            }
          },
          "parameters": {
            "__IMTCONN__": {
              "data": {
                "scoped": "true",
                "connection": "pinterest2"
              },
              "label": "pinterest Acc"
            }
          }
        },
        "parameters": [
          {
            "name": "__IMTCONN__",
            "type": "account:pinterest2",
            "label": "Connection",
            "required": true
          }
        ],
        "expect": [
          {
            "name": "limit",
            "type": "uinteger",
            "label": "Limit"
          },
          {
            "name": "ad_account_id",
            "type": "select",
            "label": "Ad Account"
          }
        ]
      }
    },
    {
      "id": 7,
      "module": "pinterest:makeAnApiCall",
      "version": 2,
      "parameters": {
        "__IMTCONN__": 1368953
      },
      "mapper": {
        "qs": [
          {
            "key": "pin_metrics",
            "value": "true"
          },
          {
            "key": "page_size",
            "value": "250"
          }
        ],
        "url": "/v5/boards/{{14.id}}/pins",
        "method": "GET",
        "headers": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "Accept",
            "value": "application/json"
          }
        ]
      },
      "metadata": {
        "designer": {
          "x": 300,
          "y": 0,
          "name": "Get 250 Pins"
        },
        "restore": {
          "expect": {
            "qs": {
              "mode": "chose",
              "items": [
                null,
                null
              ]
            },
            "body": {
              "collapsed": true
            },
            "method": {
              "mode": "chose",
              "label": "GET"
            },
            "headers": {
              "mode": "chose",
              "items": [
                null,
                null
              ],
              "collapsed": true
            }
          },
          "parameters": {
            "__IMTCONN__": {
              "data": {
                "scoped": "true",
                "connection": "pinterest2"
              },
              "label": "pinterest Acc"
            }
          }
        },
        "parameters": [
          {
            "name": "__IMTCONN__",
            "type": "account:pinterest2",
            "label": "Connection",
            "required": true
          }
        ],
        "expect": [
          {
            "name": "url",
            "type": "text",
            "label": "URL",
            "required": true
          },
          {
            "name": "method",
            "type": "select",
            "label": "Method",
            "required": true,
            "validate": {
              "enum": [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE"
              ]
            }
          },
          {
            "name": "headers",
            "spec": [
              {
                "name": "key",
                "type": "text",
                "label": "Key"
              },
              {
                "name": "value",
                "type": "text",
                "label": "Value"
              }
            ],
            "type": "array",
            "label": "Headers"
          },
          {
            "name": "qs",
            "spec": [
              {
                "name": "key",
                "type": "text",
                "label": "Key"
              },
              {
                "name": "value",
                "type": "text",
                "label": "Value"
              }
            ],
            "type": "array",
            "label": "Query String"
          },
          {
            "name": "body",
            "type": "any",
            "label": "Body"
          }
        ]
      }
    },
    {
      "id": 9,
      "module": "builtin:BasicFeeder",
      "version": 1,
      "parameters": {},
      "mapper": {
        "array": "{{7.body.items}}"
      },
      "metadata": {
        "designer": {
          "x": 600,
          "y": 0,
          "name": "Run filter for each pin"
        },
        "restore": {
          "expect": {
            "array": {
              "mode": "edit"
            }
          }
        },
        "expect": [
          {
            "mode": "edit",
            "name": "array",
            "spec": [],
            "type": "array",
            "label": "Array"
          }
        ]
      }
    },
    {
      "id": 12,
      "module": "pinterest:deletePin",
      "version": 2,
      "parameters": {
        "__IMTCONN__": 1368953
      },
      "filter": {
        "name": "Filter",
        "conditions": [
          [
            {
              "a": "{{9.pin_metrics.lifetime_metrics.impression}}",
              "o": "text:equal",
              "b": "0"
            },
            {
              "a": "{{9.created_at}}",
              "o": "date:less",
              "b": "{{addDays(now; -90)}}"
            }
          ]
        ]
      },
      "mapper": {
        "pin_id": "{{9.id}}"
      },
      "metadata": {
        "designer": {
          "x": 900,
          "y": 0,
          "name": "Delete pin when passed the filter"
        },
        "restore": {
          "expect": {
            "pin_id": {
              "mode": "edit"
            },
            "ad_account_id": {
              "mode": "chose"
            }
          },
          "parameters": {
            "__IMTCONN__": {
              "data": {
                "scoped": "true",
                "connection": "pinterest2"
              },
              "label": "pinterest Acc"
            }
          }
        },
        "parameters": [
          {
            "name": "__IMTCONN__",
            "type": "account:pinterest2",
            "label": "Connection",
            "required": true
          }
        ],
        "expect": [
          {
            "mode": "edit",
            "name": "pin_id",
            "type": "select",
            "label": "Pin",
            "required": true
          },
          {
            "name": "ad_account_id",
            "type": "select",
            "label": "Ad Account"
          }
        ]
      },
      "onerror": [
        {
          "id": 15,
          "module": "util:FunctionSleep",
          "version": 1,
          "parameters": {},
          "mapper": {
            "duration": "100"
          },
          "metadata": {
            "designer": {
              "x": 1200,
              "y": 0
            },
            "restore": {},
            "expect": [
              {
                "name": "duration",
                "type": "uinteger",
                "label": "Delay",
                "validate": {
                  "min": 1,
                  "max": 300
                },
                "required": true
              }
            ]
          }
        },
        {
          "id": 16,
          "module": "builtin:Resume",
          "version": 1,
          "parameters": {},
          "mapper": {},
          "metadata": {
            "designer": {
              "x": 1500,
              "y": 0
            },
            "restore": {}
          }
        }
      ]
    }
  ],
  "metadata": {
    "instant": false,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "autoCommitTriggerLast": true,
      "sequential": false,
      "slots": null,
      "confidential": false,
      "dataloss": false,
      "dlq": false,
      "freshVariables": false
    },
    "designer": {
      "orphans": []
    },
    "zone": "us2.make.com",
    "notes": []
  }
}
```

