#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const index_js_1 = require("@modelcontextprotocol/sdk/server/index.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const types_js_1 = require("@modelcontextprotocol/sdk/types.js");
// Hardcoded demo data
const INVENTORY = {
    oxygen_cylinders: 280,
    icu_beds: 45,
    ventilators: 28,
};
const SUPPLIERS = {
    oxygen_cylinders: { name: 'OxyGen Corp', lead_time_days: 2, available: 500 },
    icu_beds: { name: 'Medical Beds Inc', lead_time_days: 5, available: 100 },
    ventilators: { name: 'BreathTech', lead_time_days: 3, available: 50 },
};
const PURCHASE_ORDERS = [];
let PO_COUNTER = 1001;
class MCPServer {
    server;
    constructor() {
        this.server = new index_js_1.Server({
            name: 'hospital-icu-predictor-mcp',
            version: '1.0.0',
        });
        this.setupHandlers();
    }
    setupHandlers() {
        // List available tools
        this.server.setRequestHandler(types_js_1.ListToolsRequestSchema, async () => {
            const tools = [
                {
                    name: 'get_inventory',
                    description: 'Get current inventory levels for hospital resources',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            item: {
                                type: 'string',
                                enum: ['oxygen_cylinders', 'icu_beds', 'ventilators'],
                                description: 'Type of resource to check inventory for',
                            },
                        },
                        required: ['item'],
                    },
                },
                {
                    name: 'check_supplier_availability',
                    description: 'Check if a supplier has the item in stock and lead time',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            item: {
                                type: 'string',
                                enum: ['oxygen_cylinders', 'icu_beds', 'ventilators'],
                                description: 'Type of resource to check supplier availability for',
                            },
                        },
                        required: ['item'],
                    },
                },
                {
                    name: 'create_draft_purchase_order',
                    description: 'Create a draft purchase order for hospital resources',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            item: {
                                type: 'string',
                                enum: ['oxygen_cylinders', 'icu_beds', 'ventilators'],
                                description: 'Type of resource to order',
                            },
                            quantity: {
                                type: 'number',
                                minimum: 1,
                                description: 'Quantity to order',
                            },
                        },
                        required: ['item', 'quantity'],
                    },
                },
                {
                    name: 'get_pending_orders',
                    description: 'Get all pending purchase orders awaiting approval',
                    inputSchema: {
                        type: 'object',
                        properties: {},
                    },
                },
                {
                    name: 'approve_purchase_order',
                    description: 'Approve a pending purchase order',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            po_id: {
                                type: 'string',
                                description: 'Purchase order ID to approve',
                            },
                        },
                        required: ['po_id'],
                    },
                },
            ];
            return { tools };
        });
        // Handle tool calls
        this.server.setRequestHandler(types_js_1.CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;
            try {
                switch (name) {
                    case 'get_inventory':
                        return this.handleGetInventory(args);
                    case 'check_supplier_availability':
                        return this.handleCheckSupplierAvailability(args);
                    case 'create_draft_purchase_order':
                        return this.handleCreateDraftPO(args);
                    case 'get_pending_orders':
                        return this.handleGetPendingOrders();
                    case 'approve_purchase_order':
                        return this.handleApprovePO(args);
                    default:
                        throw new Error(`Unknown tool: ${name}`);
                }
            }
            catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Error: ${errorMessage}`,
                        },
                    ],
                    isError: true,
                };
            }
        });
    }
    handleGetInventory(args) {
        const { item } = args;
        if (!item || !INVENTORY.hasOwnProperty(item)) {
            throw new Error(`Invalid item: ${item}. Must be one of: oxygen_cylinders, icu_beds, ventilators`);
        }
        const quantity = INVENTORY[item];
        const daysSupply = item === 'oxygen_cylinders' ? (quantity / 150).toFixed(1) : 'N/A';
        return {
            content: [
                {
                    type: 'text',
                    text: `📦 Current Inventory for ${item.replace(/_/g, ' ')}:
          
Current Stock: ${quantity} units
Days of Supply: ${daysSupply}
Status: ${quantity < 150 ? '⚠️ LOW' : '✅ ADEQUATE'}`,
                },
            ],
            isError: false,
        };
    }
    handleCheckSupplierAvailability(args) {
        const { item } = args;
        if (!item || !SUPPLIERS.hasOwnProperty(item)) {
            throw new Error(`Invalid item: ${item}`);
        }
        const supplier = SUPPLIERS[item];
        return {
            content: [
                {
                    type: 'text',
                    text: `🏭 Supplier Information for ${item.replace(/_/g, ' ')}:
          
Supplier: ${supplier.name}
Available Stock: ${supplier.available} units
Lead Time: ${supplier.lead_time_days} days
Status: ${supplier.available > 0 ? '✅ IN STOCK' : '❌ OUT OF STOCK'}`,
                },
            ],
            isError: false,
        };
    }
    handleCreateDraftPO(args) {
        const { item, quantity } = args;
        if (!item || !quantity || quantity < 1) {
            throw new Error('Valid item and quantity (>= 1) required');
        }
        if (!SUPPLIERS.hasOwnProperty(item)) {
            throw new Error(`Invalid item: ${item}`);
        }
        const poId = `PO-${PO_COUNTER++}`;
        const supplier = SUPPLIERS[item];
        const estimatedDelivery = new Date();
        estimatedDelivery.setDate(estimatedDelivery.getDate() + supplier.lead_time_days);
        const po = {
            po_id: poId,
            item,
            quantity,
            supplier: supplier.name,
            status: 'PENDING_APPROVAL',
            created_at: new Date().toISOString(),
            estimated_delivery: estimatedDelivery.toISOString().split('T')[0],
        };
        PURCHASE_ORDERS.push(po);
        return {
            content: [
                {
                    type: 'text',
                    text: `📋 Draft Purchase Order Created:

PO ID: ${poId}
Item: ${item.replace(/_/g, ' ')}
Quantity: ${quantity}
Supplier: ${supplier.name}
Lead Time: ${supplier.lead_time_days} days
Estimated Delivery: ${estimatedDelivery.toISOString().split('T')[0]}
Status: ⏳ PENDING_APPROVAL

⚠️ This order is in DRAFT status. Admin must approve in dashboard.`,
                },
            ],
            isError: false,
        };
    }
    handleGetPendingOrders() {
        const pendingOrders = PURCHASE_ORDERS.filter(po => po.status === 'PENDING_APPROVAL');
        if (pendingOrders.length === 0) {
            return {
                content: [
                    {
                        type: 'text',
                        text: '✅ No pending orders awaiting approval.',
                    },
                ],
                isError: false,
            };
        }
        const ordersText = pendingOrders
            .map(po => `
🔹 ${po.po_id}
   Item: ${po.item.replace(/_/g, ' ')}
   Quantity: ${po.quantity}
   Supplier: ${po.supplier}
   Est. Delivery: ${po.estimated_delivery}`)
            .join('\n');
        return {
            content: [
                {
                    type: 'text',
                    text: `📋 Pending Purchase Orders (${pendingOrders.length}):${ordersText}`,
                },
            ],
            isError: false,
        };
    }
    handleApprovePO(args) {
        const { po_id } = args;
        const po = PURCHASE_ORDERS.find(p => p.po_id === po_id);
        if (!po) {
            throw new Error(`Purchase order not found: ${po_id}`);
        }
        if (po.status !== 'PENDING_APPROVAL') {
            throw new Error(`Order ${po_id} is already ${po.status}`);
        }
        po.status = 'APPROVED';
        return {
            content: [
                {
                    type: 'text',
                    text: `✅ Purchase Order Approved:

PO ID: ${po.po_id}
Item: ${po.item.replace(/_/g, ' ')}
Quantity: ${po.quantity}
Status: ✅ APPROVED
Estimated Delivery: ${po.estimated_delivery}

Order has been sent to supplier.`,
                },
            ],
            isError: false,
        };
    }
    async start() {
        const transport = new stdio_js_1.StdioServerTransport();
        await this.server.connect(transport);
        console.error('🏥 Hospital ICU Predictor MCP Server started successfully');
    }
}
// Start the server
const server = new MCPServer();
server.start().catch((error) => {
    console.error('Failed to start MCP server:', error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map