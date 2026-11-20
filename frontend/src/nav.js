// Sidebar structure of the GIS portal.
// `type` maps to the backend asset_type (or a dedicated page later).
export const NAV = [
  { section: "CORE", items: [
    { label: "Overview", to: "/" },
    { label: "Sites", to: "/assets/SITE" },
  ]},
  { section: "NETWORK", items: [
    { label: "OLT", to: "/assets/OLT" },
    { label: "PON Ports", to: "/assets/PON_PORT" },
    { label: "ODF", to: "/assets/ODF" },
    { label: "ODF Ports", to: "/assets/ODF_PORT" },
    { label: "Splitter", to: "/assets/SPLITTER" },
    { label: "Splitter Ports", to: "/assets/SPLITTER_PORT" },
    { label: "FAT / FDB", to: "/assets/FAT" },
    { label: "FAT Ports", to: "/assets/FAT_PORT" },
    { label: "Network Devices", to: "/assets/NETWORK_DEVICE" },
    { label: "Interfaces", to: "/assets/INTERFACE" },
  ]},
  { section: "FIBER", items: [
    { label: "Fiber Cables", to: "/assets/CABLE" },
    { label: "Fiber Cores", to: "/assets/CORE" },
    { label: "Splice Closures", to: "/assets/SPLICE_CLOSURE" },
  ]},
  { section: "CUSTOMERS", items: [
    { label: "ONT", to: "/assets/ONT" },
    { label: "Customers", to: "/assets/CUSTOMER" },
    { label: "Customer Devices", to: "/assets/CUSTOMER_DEVICE" },
    { label: "Customer Services", to: "/assets/CUSTOMER_SERVICE" },
  ]},
  { section: "PHYSICAL", items: [
    { label: "Poles", to: "/assets/POLE" },
    { label: "Manholes", to: "/assets/MANHOLE" },
  ]},
  { section: "TOOLS", items: [
    { label: "Trace", to: "/assets/TRACE" },
    { label: "Reports", to: "/assets/REPORTS" },
    { label: "Settings", to: "/assets/SETTINGS" },
  ]},
];
