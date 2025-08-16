import React, { useEffect, useMemo, useState } from "react";

// Pharmacist Agency App — Single‑file React prototype (MVP)
// Features: search, filters, shortlist, compare (up to 4), RFQ composer, basic notifications
// Styling: Tailwind CSS utility classes
// Notes: All data is mocked in-memory; replace with API calls later

// Types
type RateUnit = "hr" | "shift" | "day";

type RateCard = {
  shift: "day" | "night" | "weekend" | "on_call";
  amount: number; // numeric amount in currency unit
  unit: RateUnit;
  currency: string; // e.g., INR, USD
  surgePct?: number; // optional surge percent
};

export type Agency = {
  id: string;
  name: string;
  verified: boolean;
  rating: number; // 0..5
  ratingCount: number;
  regions: string[];
  specialties: string[];
  availability: string; // human friendly for MVP
  badges?: string[];
  rates: RateCard[];
  lastUpdated: string; // ISO date string
};

// Mock data
const AGENCIES: Agency[] = [
  {
    id: "ag_medi_1",
    name: "MediStaff Connect",
    verified: true,
    rating: 4.6,
    ratingCount: 128,
    regions: ["Mumbai", "Pune"],
    specialties: ["Oncology", "Emergency"],
    availability: "24/7",
    badges: ["Emergency", "Weekend"],
    lastUpdated: "2025-08-12",
    rates: [
      { shift: "day", amount: 420, unit: "shift", currency: "INR" },
      { shift: "night", amount: 520, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 600, unit: "shift", currency: "INR", surgePct: 10 },
      { shift: "on_call", amount: 70, unit: "hr", currency: "INR" },
    ],
  },
  {
    id: "ag_care_2",
    name: "CarePlus Agency",
    verified: true,
    rating: 4.2,
    ratingCount: 86,
    regions: ["Mumbai"],
    specialties: ["General", "ICU"],
    availability: "Weekdays",
    badges: ["ICU"],
    lastUpdated: "2025-08-10",
    rates: [
      { shift: "day", amount: 410, unit: "shift", currency: "INR" },
      { shift: "night", amount: 500, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 590, unit: "shift", currency: "INR" },
    ],
  },
  {
    id: "ag_night_3",
    name: "NightShift Pros",
    verified: false,
    rating: 4.7,
    ratingCount: 45,
    regions: ["Pune", "Nashik"],
    specialties: ["Emergency", "ICU"],
    availability: "Nights + Weekends",
    badges: ["Emergency", "Night"],
    lastUpdated: "2025-08-09",
    rates: [
      { shift: "night", amount: 510, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 605, unit: "shift", currency: "INR" },
      { shift: "on_call", amount: 75, unit: "hr", currency: "INR" },
    ],
  },
  {
    id: "ag_city_4",
    name: "CityCare Network",
    verified: true,
    rating: 4.0,
    ratingCount: 210,
    regions: ["Mumbai", "Thane"],
    specialties: ["General"],
    availability: "24/7",
    badges: ["General"],
    lastUpdated: "2025-08-13",
    rates: [
      { shift: "day", amount: 380, unit: "shift", currency: "INR" },
      { shift: "night", amount: 460, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 540, unit: "shift", currency: "INR" },
    ],
  },
  {
    id: "ag_prime_5",
    name: "Prime Med Staffing",
    verified: true,
    rating: 4.8,
    ratingCount: 59,
    regions: ["Pune"],
    specialties: ["Oncology"],
    availability: "Weekdays",
    badges: ["Oncology"],
    lastUpdated: "2025-08-08",
    rates: [
      { shift: "day", amount: 460, unit: "shift", currency: "INR" },
      { shift: "night", amount: 540, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 630, unit: "shift", currency: "INR" },
    ],
  },
  {
    id: "ag_speed_6",
    name: "Rapid Relief Medics",
    verified: false,
    rating: 3.9,
    ratingCount: 33,
    regions: ["Mumbai", "Navi Mumbai"],
    specialties: ["Emergency"],
    availability: "24/7",
    badges: ["Emergency"],
    lastUpdated: "2025-08-06",
    rates: [
      { shift: "day", amount: 400, unit: "shift", currency: "INR" },
      { shift: "night", amount: 490, unit: "shift", currency: "INR" },
      { shift: "on_call", amount: 68, unit: "hr", currency: "INR" },
    ],
  },
  {
    id: "ag_elite_7",
    name: "Elite Health Partners",
    verified: true,
    rating: 4.4,
    ratingCount: 102,
    regions: ["Nashik"],
    specialties: ["ICU", "Emergency"],
    availability: "Rotational",
    badges: ["ICU"],
    lastUpdated: "2025-08-03",
    rates: [
      { shift: "day", amount: 430, unit: "shift", currency: "INR" },
      { shift: "night", amount: 515, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 595, unit: "shift", currency: "INR" },
    ],
  },
  {
    id: "ag_green_8",
    name: "GreenCross Alliance",
    verified: true,
    rating: 4.1,
    ratingCount: 78,
    regions: ["Thane", "Navi Mumbai"],
    specialties: ["General"],
    availability: "Weekends",
    badges: ["Weekend"],
    lastUpdated: "2025-08-11",
    rates: [
      { shift: "day", amount: 395, unit: "shift", currency: "INR" },
      { shift: "night", amount: 470, unit: "shift", currency: "INR" },
      { shift: "weekend", amount: 555, unit: "shift", currency: "INR" },
    ],
  },
];

// Helpers
const currency = (amount: number, ccy = "INR") =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: ccy, maximumFractionDigits: 0 }).format(amount);

const badgeColor = (label: string) => {
  const map: Record<string, string> = {
    Emergency: "bg-red-50 text-red-600",
    Weekend: "bg-amber-50 text-amber-700",
    Oncology: "bg-fuchsia-50 text-fuchsia-700",
    ICU: "bg-blue-50 text-blue-700",
    Night: "bg-slate-100 text-slate-700",
    General: "bg-emerald-50 text-emerald-700",
    Verified: "bg-green-50 text-green-700",
  };
  return map[label] || "bg-slate-100 text-slate-700";
};

// Components
function Pill({ children, className = "" }: React.PropsWithChildren<{ className?: string }>) {
  return <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${className}`}>{children}</span>;
}

function Section({ title, children, action }: React.PropsWithChildren<{ title: string; action?: React.ReactNode }>) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4 md:p-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg md:text-xl font-semibold text-slate-800">{title}</h2>
        {action}
      </div>
      {children}
    </div>
  );
}

function StarRating({ value }: { value: number }) {
  const full = Math.floor(value);
  const half = value - full >= 0.5;
  return (
    <div className="flex items-center gap-0.5" aria-label={`Rating ${value.toFixed(1)}`}>
      {Array.from({ length: 5 }).map((_, i) => (
        <span key={i} className={`text-yellow-500 ${i < full ? "opacity-100" : i === full && half ? "opacity-70" : "opacity-30"}`}>
          ★
        </span>
      ))}
      <span className="ml-1 text-xs text-slate-600">{value.toFixed(1)}</span>
    </div>
  );
}

function RateRow({ label, rate }: { label: string; rate?: RateCard }) {
  return (
    <div className="flex items-center justify-between text-sm py-1">
      <span className="text-slate-600">{label}</span>
      <span className="font-medium text-slate-800">{rate ? `${currency(rate.amount, rate.currency)} / ${rate.unit}` : "—"}</span>
    </div>
  );
}

function AgencyCard({ agency, onCompareToggle, selectedForCompare, onSave, onOpenProfile }: {
  agency: Agency;
  onCompareToggle: (id: string) => void;
  selectedForCompare: boolean;
  onSave: (agency: Agency) => void;
  onOpenProfile: (agency: Agency) => void;
}) {
  const day = agency.rates.find(r => r.shift === "day");
  const night = agency.rates.find(r => r.shift === "night");
  const weekend = agency.rates.find(r => r.shift === "weekend");

  return (
    <div className="border border-slate-100 rounded-2xl p-4 bg-white shadow-sm hover:shadow-md transition">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base md:text-lg font-semibold text-slate-800">{agency.name}</h3>
            {agency.verified && <Pill className={badgeColor("Verified")}>Verified</Pill>}
          </div>
          <div className="mt-1"><StarRating value={agency.rating} /> <span className="text-xs text-slate-500 ml-1">({agency.ratingCount})</span></div>
          <div className="mt-1 text-xs text-slate-600">Regions: {agency.regions.join(", ")}</div>
          <div className="mt-1 flex flex-wrap gap-1">
            {agency.badges?.map(b => (
              <Pill key={b} className={badgeColor(b)}>{b}</Pill>
            ))}
          </div>
        </div>
        <div className="text-right text-xs text-slate-500">Updated {new Date(agency.lastUpdated).toLocaleDateString()}</div>
      </div>

      <div className="mt-3 divide-y">
        <RateRow label="Day" rate={day} />
        <RateRow label="Night" rate={night} />
        <RateRow label="Weekend" rate={weekend} />
      </div>

      <div className="mt-4 flex gap-2">
        <button onClick={() => onOpenProfile(agency)} className="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-sm">View Profile</button>
        <button onClick={() => onSave(agency)} className="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm">Save</button>
        <button onClick={() => onCompareToggle(agency.id)} className={`px-3 py-2 rounded-xl text-sm ${selectedForCompare ? "bg-indigo-600 text-white" : "bg-indigo-50 text-indigo-700 hover:bg-indigo-100"}`}>{selectedForCompare ? "Remove" : "Compare"}</button>
      </div>
    </div>
  );
}

function CompareTable({ agencies, onClose }: { agencies: Agency[]; onClose: () => void }) {
  const get = (a: Agency, shift: RateCard["shift"]) => a.rates.find(r => r.shift === shift);
  const rows: { label: string; getVal: (a: Agency) => string | number | React.ReactNode }[] = [
    { label: "Day Rate", getVal: a => {
      const r = get(a, "day");
      return r ? `${currency(r.amount, r.currency)} / ${r.unit}` : "—";
    } },
    { label: "Night Rate", getVal: a => {
      const r = get(a, "night");
      return r ? `${currency(r.amount, r.currency)} / ${r.unit}` : "—";
    } },
    { label: "Weekend", getVal: a => {
      const r = get(a, "weekend");
      return r ? `${currency(r.amount, r.currency)} / ${r.unit}` : "—";
    } },
    { label: "Availability", getVal: a => a.availability },
    { label: "Rating", getVal: a => (
      <span className="inline-flex items-center gap-1"><StarRating value={a.rating} /><span className="text-xs text-slate-500">({a.ratingCount})</span></span>
    ) },
  ];

  return (
    <div className="fixed inset-0 z-40 bg-black/40 flex items-end md:items-center justify-center p-2 md:p-6" role="dialog" aria-modal>
      <div className="bg-white w-full md:max-w-5xl rounded-2xl shadow-xl p-4 md:p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg md:text-xl font-semibold">Compare Agencies</h3>
          <button onClick={onClose} className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200">Close</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr>
                <th className="text-left p-2 text-slate-500">Metric</th>
                {agencies.map(a => (
                  <th key={a.id} className="text-left p-2">{a.name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map(row => (
                <tr key={row.label} className="odd:bg-slate-50/50">
                  <td className="p-2 text-slate-600 w-40">{row.label}</td>
                  {agencies.map(a => (
                    <td key={a.id + row.label} className="p-2">{row.getVal(a)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function RFQModal({ open, onClose, agencies }: { open: boolean; onClose: () => void; agencies: Agency[] }) {
  const [message, setMessage] = useState("");
  const [deadline, setDeadline] = useState("");

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-40 bg-black/40 flex items-end md:items-center justify-center p-2 md:p-6" role="dialog" aria-modal>
      <div className="bg-white w-full md:max-w-2xl rounded-2xl shadow-xl p-4 md:p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg md:text-xl font-semibold">Send RFQ to {agencies.length} agenc{agencies.length === 1 ? "y" : "ies"}</h3>
          <button onClick={onClose} className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200">Close</button>
        </div>
        <div className="space-y-3">
          <div>
            <label className="text-sm text-slate-600">Deadline</label>
            <input type="date" value={deadline} onChange={e => setDeadline(e.target.value)} className="mt-1 w-full px-3 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="text-sm text-slate-600">Message / Requirements</label>
            <textarea rows={5} value={message} onChange={e => setMessage(e.target.value)} className="mt-1 w-full px-3 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Describe shift types, dates, certifications, and any constraints..." />
          </div>
          <button onClick={() => {
            alert(`RFQ sent to ${agencies.map(a => a.name).join(", ")}\nDeadline: ${deadline || "(none)"}\nMessage: ${message || "(empty)"}`);
            onClose();
          }} className="w-full md:w-auto px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white">Send RFQ</button>
        </div>
      </div>
    </div>
  );
}

function ProfileDrawer({ agency, onClose }: { agency: Agency | null; onClose: () => void }) {
  if (!agency) return null;
  const day = agency.rates.find(r => r.shift === "day");
  const night = agency.rates.find(r => r.shift === "night");
  const weekend = agency.rates.find(r => r.shift === "weekend");

  return (
    <div className="fixed inset-0 z-40 flex">
      <div className="flex-1 bg-black/40" onClick={onClose} />
      <div className="w-full max-w-md bg-white h-full shadow-xl p-4 md:p-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg md:text-xl font-semibold">{agency.name}</h3>
          <button onClick={onClose} className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200">Close</button>
        </div>
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            {agency.verified && <Pill className={badgeColor("Verified")}>Verified</Pill>}
            {agency.badges?.map(b => <Pill key={b} className={badgeColor(b)}>{b}</Pill>)}
          </div>
          <div className="text-sm text-slate-600">Regions: {agency.regions.join(", ")}</div>
          <div>
            <h4 className="font-medium text-slate-800">Rates</h4>
            <div className="mt-2 space-y-1 text-sm">
              <div>Day: {day ? `${currency(day.amount, day.currency)} / ${day.unit}` : "—"}</div>
              <div>Night: {night ? `${currency(night.amount, night.currency)} / ${night.unit}` : "—"}</div>
              <div>Weekend: {weekend ? `${currency(weekend.amount, weekend.currency)} / ${weekend.unit}` : "—"}</div>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-slate-800">Specialties</h4>
            <div className="mt-2 flex flex-wrap gap-1">
              {agency.specialties.map(s => <Pill key={s} className={badgeColor(s)}>{s}</Pill>)}
            </div>
          </div>
          <div>
            <h4 className="font-medium text-slate-800">Availability</h4>
            <p className="text-sm text-slate-700 mt-1">{agency.availability}</p>
          </div>
          <div className="text-xs text-slate-500">Last updated {new Date(agency.lastUpdated).toLocaleDateString()}</div>
        </div>
      </div>
    </div>
  );
}

export default function PharmacistAgencyApp() {
  // Search & filters
  const [query, setQuery] = useState("");
  const [region, setRegion] = useState("all");
  const [specialty, setSpecialty] = useState("all");
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const [shiftType, setShiftType] = useState<"any" | RateCard["shift"]>("any");
  const [maxRate, setMaxRate] = useState<number | null>(null);

  // Compare & shortlist & RFQ
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [showCompare, setShowCompare] = useState(false);
  const [showRFQ, setShowRFQ] = useState(false);
  const [profileAgency, setProfileAgency] = useState<Agency | null>(null);
  const [saved, setSaved] = useState<Record<string, boolean>>({});

  // Notifications (mock)
  const [notifsOpen, setNotifsOpen] = useState(false);
  const [notifs] = useState<{ id: string; text: string; date: string }[]>([
    { id: "n1", text: "MediStaff Connect increased night shift by 5%", date: "2025-08-12" },
    { id: "n2", text: "GreenCross updated weekend rates", date: "2025-08-11" },
  ]);

  // Derived options
  const regions = useMemo(() => Array.from(new Set(AGENCIES.flatMap(a => a.regions))), []);
  const specialties = useMemo(() => Array.from(new Set(AGENCIES.flatMap(a => a.specialties))), []);

  // Filtering
  const filtered = useMemo(() => {
    return AGENCIES.filter(a => {
      if (verifiedOnly && !a.verified) return false;
      if (region !== "all" && !a.regions.includes(region)) return false;
      if (specialty !== "all" && !a.specialties.includes(specialty)) return false;
      if (query && !a.name.toLowerCase().includes(query.toLowerCase())) return false;
      if (shiftType !== "any") {
        const r = a.rates.find(rr => rr.shift === shiftType);
        if (!r) return false;
        if (maxRate !== null && r.amount > maxRate) return false;
      } else if (maxRate !== null) {
        // if no specific shift, check minimum available rate against max
        const min = Math.min(...a.rates.map(r => r.amount));
        if (min > maxRate) return false;
      }
      return true;
    });
  }, [query, region, specialty, verifiedOnly, shiftType, maxRate]);

  // Compare handlers
  const toggleCompare = (id: string) => {
    setCompareIds(prev => {
      if (prev.includes(id)) return prev.filter(x => x !== id);
      if (prev.length >= 4) return prev; // max 4
      return [...prev, id];
    });
  };

  const selectedForCompare = AGENCIES.filter(a => compareIds.includes(a.id));

  // Save handler
  const saveAgency = (a: Agency) => setSaved(prev => ({ ...prev, [a.id]: true }));

  // Keyboard: ESC to close overlays
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") { setShowCompare(false); setShowRFQ(false); setProfileAgency(null); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Top bar */}
      <header className="sticky top-0 z-30 bg-white/80 backdrop-blur border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-3 md:px-6 py-3 flex items-center gap-2 md:gap-4">
          <div className="flex items-center gap-2 font-bold text-slate-800 text-lg md:text-xl">
            <span className="inline-flex items-center justify-center w-8 h-8 rounded-xl bg-indigo-600 text-white">Rx</span>
            <span>Agency Compare</span>
          </div>
          <div className="flex-1" />
          <button onClick={() => setNotifsOpen(v => !v)} className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-sm">🔔 Notifications</button>
          <div className="w-8 h-8 rounded-full bg-slate-200" />
        </div>
        {notifsOpen && (
          <div className="max-w-6xl mx-auto px-3 md:px-6 pb-3">
            <Section title="Recent changes">
              <ul className="text-sm text-slate-700 list-disc pl-5">
                {notifs.map(n => (
                  <li key={n.id} className="py-0.5">{n.text} <span className="text-xs text-slate-500">({new Date(n.date).toLocaleDateString()})</span></li>
                ))}
              </ul>
            </Section>
          </div>
        )}
      </header>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-3 md:px-6 py-4 md:py-6 space-y-4">
        {/* Search & Filters */}
        <Section title="Find agencies" action={<button onClick={() => { setQuery(""); setRegion("all"); setSpecialty("all"); setVerifiedOnly(false); setShiftType("any"); setMaxRate(null); }} className="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-sm">Reset</button>}>
          <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
            <div className="md:col-span-2">
              <label className="text-sm text-slate-600">Search by name</label>
              <input value={query} onChange={e => setQuery(e.target.value)} placeholder="e.g. MediStaff" className="mt-1 w-full px-3 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
              <label className="text-sm text-slate-600">Region</label>
              <select value={region} onChange={e => setRegion(e.target.value)} className="mt-1 w-full px-3 py-2 border rounded-xl">
                <option value="all">All</option>
                {regions.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm text-slate-600">Specialty</label>
              <select value={specialty} onChange={e => setSpecialty(e.target.value)} className="mt-1 w-full px-3 py-2 border rounded-xl">
                <option value="all">All</option>
                {specialties.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm text-slate-600">Shift</label>
              <select value={shiftType} onChange={e => setShiftType(e.target.value as any)} className="mt-1 w-full px-3 py-2 border rounded-xl">
                <option value="any">Any</option>
                <option value="day">Day</option>
                <option value="night">Night</option>
                <option value="weekend">Weekend</option>
                <option value="on_call">On‑call</option>
              </select>
            </div>
            <div>
              <label className="text-sm text-slate-600">Max rate (₹)</label>
              <input type="number" min={0} value={maxRate ?? ""} onChange={e => setMaxRate(e.target.value ? Number(e.target.value) : null)} className="mt-1 w-full px-3 py-2 border rounded-xl" placeholder="e.g. 500" />
            </div>
            <div className="flex items-end gap-2">
              <label className="inline-flex items-center gap-2 text-sm text-slate-700 mb-2">
                <input type="checkbox" checked={verifiedOnly} onChange={e => setVerifiedOnly(e.target.checked)} /> Verified only
              </label>
            </div>
          </div>
        </Section>

        {/* Results */}
        <Section title={`Agencies (${filtered.length})`}>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
            {filtered.map(agency => (
              <div key={agency.id} className="relative">
                {saved[agency.id] && <div className="absolute top-2 right-2"><Pill className="bg-emerald-100 text-emerald-700">Saved</Pill></div>}
                <AgencyCard
                  agency={agency}
                  onCompareToggle={toggleCompare}
                  selectedForCompare={compareIds.includes(agency.id)}
                  onSave={saveAgency}
                  onOpenProfile={setProfileAgency}
                />
              </div>
            ))}
          </div>
          {filtered.length === 0 && (
            <div className="text-center py-10 text-slate-600">No agencies match your filters.</div>
          )}
        </Section>
      </main>

      {/* Compare tray */}
      <div className={`fixed bottom-3 left-0 right-0 transition ${compareIds.length ? "opacity-100" : "opacity-0 pointer-events-none"}`}>
        <div className="max-w-6xl mx-auto px-3 md:px-6">
          <div className="bg-white border border-slate-200 rounded-2xl shadow-lg p-3 md:p-4 flex items-center gap-2">
            <div className="font-medium">Compare ({compareIds.length}/4)</div>
            <div className="flex-1 flex flex-wrap gap-2">
              {compareIds.map(id => {
                const a = AGENCIES.find(x => x.id === id)!;
                return (
                  <div key={id} className="px-2 py-1 rounded-xl bg-slate-100 text-sm flex items-center gap-2">
                    <span>{a.name}</span>
                    <button onClick={() => setCompareIds(prev => prev.filter(x => x !== id))} className="text-slate-500 hover:text-slate-700">✕</button>
                  </div>
                );
              })}
            </div>
            <button onClick={() => setShowCompare(true)} disabled={!compareIds.length} className="px-3 py-2 rounded-xl bg-indigo-600 disabled:bg-indigo-300 text-white">Open</button>
            <button onClick={() => setShowRFQ(true)} disabled={!compareIds.length} className="px-3 py-2 rounded-xl bg-emerald-600 disabled:bg-emerald-300 text-white">Send RFQ</button>
          </div>
        </div>
      </div>

      {/* Overlays */}
      {showCompare && <CompareTable agencies={selectedForCompare} onClose={() => setShowCompare(false)} />}
      <RFQModal open={showRFQ} onClose={() => setShowRFQ(false)} agencies={selectedForCompare} />
      <ProfileDrawer agency={profileAgency} onClose={() => setProfileAgency(null)} />

      <footer className="py-8 text-center text-xs text-slate-500">© 2025 Agency Compare MVP · Demo data</footer>
    </div>
  );
}
