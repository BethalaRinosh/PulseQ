import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, Bell, CalendarDays,
  Check, ChevronDown, ChevronLeft, ChevronRight, CircleHelp, Clock3, Command,
  FileText, Filter, HeartPulse, LayoutDashboard, Menu, MoreHorizontal,
  Plus, Search, Settings2, ShieldCheck, Stethoscope, UserRound, Users,
  X, Zap, BedDouble, ClipboardList, ArrowUpDown, Siren, RefreshCw,
  UserPlus, ListOrdered, Sparkles, CircleCheck, AlertCircle, LoaderCircle,
  LogOut, PanelLeftClose, PanelLeftOpen
} from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const payload = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) throw new Error(payload?.detail || "The request could not be completed.");
  return payload;
}

const cx = (...values) => values.filter(Boolean).join(" ");
const initials = (name = "") => name.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase() || "PQ";
const colors = ["bg-teal-50 text-teal-700", "bg-amber-50 text-amber-600", "bg-rose-50 text-rose-600", "bg-slate-100 text-slate-600"];

function Button({ children, variant = "primary", className = "", ...props }) {
  const styles = {
    primary: "bg-ink text-white hover:bg-[#344341] shadow-sm",
    secondary: "border border-line bg-white text-ink hover:bg-slate-50",
    subtle: "text-muted hover:bg-slate-100 hover:text-ink",
    teal: "bg-teal-600 text-white hover:bg-teal-700",
    danger: "border border-rose-100 bg-rose-50 text-rose-600 hover:bg-rose-100",
  };
  return <button className={cx("inline-flex items-center justify-center gap-2 rounded-xl px-3.5 py-2.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50", styles[variant], className)} {...props}>{children}</button>;
}

function Status({ children, tone = "neutral" }) {
  const tones = {
    neutral: "bg-slate-100 text-slate-600",
    teal: "bg-teal-50 text-teal-700",
    amber: "bg-amber-50 text-amber-600",
    rose: "bg-rose-50 text-rose-600",
  };
  return <span className={cx("inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-bold tracking-wide", tones[tone])}><span className={cx("h-1.5 w-1.5 rounded-full", tone === "teal" ? "bg-teal-500" : tone === "amber" ? "bg-amber-600" : tone === "rose" ? "bg-rose-600" : "bg-slate-400")} />{children}</span>;
}

function Avatar({ name, size = "md", tone }) {
  return <div className={cx("flex shrink-0 items-center justify-center rounded-xl font-bold", size === "lg" ? "h-12 w-12 text-sm" : size === "sm" ? "h-8 w-8 rounded-lg text-[10px]" : "h-10 w-10 text-xs", tone || colors[(name?.charCodeAt(0) || 0) % colors.length])}>{initials(name)}</div>;
}

function SectionHeading({ eyebrow, title, description, action }) {
  return <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between"><div><div className="mb-1.5 text-[10px] font-bold uppercase tracking-[0.18em] text-teal-600">{eyebrow}</div><h1 className="font-display text-2xl font-extrabold tracking-tight text-ink sm:text-[28px]">{title}</h1>{description && <p className="mt-1.5 text-sm text-muted">{description}</p>}</div>{action}</div>;
}

function Panel({ children, className = "" }) {
  return <section className={cx("rounded-2xl border border-line bg-white shadow-soft", className)}>{children}</section>;
}

function PanelTitle({ icon: Icon, title, note, action }) {
  return <div className="flex items-center justify-between gap-3 border-b border-line px-5 py-4"><div className="flex min-w-0 items-center gap-3"><div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-canvas text-teal-700"><Icon size={17} strokeWidth={1.9} /></div><div className="min-w-0"><h2 className="truncate text-sm font-bold text-ink">{title}</h2>{note && <p className="mt-0.5 text-xs text-muted">{note}</p>}</div></div>{action}</div>;
}

function EmptyState({ icon: Icon = ClipboardList, title, text, action }) {
  return <div className="flex flex-col items-center justify-center px-5 py-12 text-center"><div className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-canvas text-muted"><Icon size={21} /></div><p className="text-sm font-bold text-ink">{title}</p><p className="mt-1 max-w-xs text-xs leading-5 text-muted">{text}</p>{action && <div className="mt-4">{action}</div>}</div>;
}

function Modal({ title, subtitle, onClose, children, width = "max-w-xl" }) {
  useEffect(() => {
    const close = (event) => event.key === "Escape" && onClose();
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, [onClose]);
  return <div className="fixed inset-0 z-50 flex items-end justify-center bg-ink/35 p-0 backdrop-blur-[3px] sm:items-center sm:p-5" onMouseDown={(e) => e.target === e.currentTarget && onClose()}><div className={cx("max-h-[92vh] w-full overflow-y-auto rounded-t-3xl border border-line bg-white shadow-2xl sm:rounded-3xl", width)}><div className="sticky top-0 z-10 flex items-start justify-between border-b border-line bg-white/95 px-6 py-5 backdrop-blur"><div><h2 className="font-display text-lg font-extrabold text-ink">{title}</h2>{subtitle && <p className="mt-1 text-sm text-muted">{subtitle}</p>}</div><button onClick={onClose} className="rounded-xl p-2 text-muted transition hover:bg-canvas hover:text-ink" aria-label="Close dialog"><X size={18} /></button></div><div className="p-6">{children}</div></div></div>;
}

function Field({ label, children, hint }) {
  return <label className="block"><span className="mb-1.5 block text-xs font-bold text-ink">{label}</span>{children}{hint && <span className="mt-1 block text-[11px] text-muted">{hint}</span>}</label>;
}

const inputClass = "w-full rounded-xl border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none transition placeholder:text-slate-400 focus:border-teal-500 focus:ring-4 focus:ring-teal-50";
const navItems = [
  { id: "Overview", icon: LayoutDashboard, label: "Overview" },
  { id: "Patients", icon: Users, label: "Patients" },
  { id: "Queue desk", icon: ListOrdered, label: "Queue desk", marker: true },
  { id: "Doctors", icon: Stethoscope, label: "Doctors" },
  { id: "DSA lab", icon: ArrowUpDown, label: "DSA lab" },
];

function PatientForm({ initial, onSubmit, busy }) {
  const [form, setForm] = useState(initial || { patient_id: "", name: "", age: "", sex: "Prefer not to say", contact: "", reason: "" });
  const set = (key) => (e) => setForm((prev) => ({ ...prev, [key]: e.target.value }));
  const submit = (e) => { e.preventDefault(); onSubmit({ ...form, age: Number(form.age) }); };
  return <form onSubmit={submit} className="space-y-5">
    <div className="grid gap-4 sm:grid-cols-2">
      <Field label="Patient ID"><input required maxLength="32" className={inputClass} placeholder="e.g. PQ-1042" value={form.patient_id} onChange={set("patient_id")} disabled={Boolean(initial)} /></Field>
      <Field label="Full name"><input required maxLength="100" className={inputClass} placeholder="Name for demo record" value={form.name} onChange={set("name")} /></Field>
      <Field label="Age" hint="Must be between 0 and 130"><input required type="number" min="0" max="130" className={inputClass} placeholder="Age" value={form.age} onChange={set("age")} /></Field>
      <Field label="Sex / gender label"><select className={inputClass} value={form.sex} onChange={set("sex")}><option>Prefer not to say</option><option>Female</option><option>Male</option><option>Non-binary</option><option>Other</option></select></Field>
      <Field label="Contact"><input required maxLength="60" className={inputClass} placeholder="Use fictional contact details" value={form.contact} onChange={set("contact")} /></Field>
      <Field label="Reason for visit"><input required maxLength="240" className={inputClass} placeholder="Demo reason only" value={form.reason} onChange={set("reason")} /></Field>
    </div>
    <div className="flex items-center justify-between border-t border-line pt-4"><p className="max-w-xs text-[11px] leading-4 text-muted">Use synthetic data only. This prototype is not for real patient care.</p><div className="flex gap-2"><Button type="submit" disabled={busy}>{busy ? <LoaderCircle size={15} className="animate-spin" /> : <Check size={15} />}{initial ? "Save changes" : "Add patient"}</Button></div></div>
  </form>;
}

function DoctorForm({ onSubmit, busy }) {
  const [form, setForm] = useState({ doctor_id: "", name: "", specialization: "", contact: "" });
  const set = (key) => (e) => setForm((prev) => ({ ...prev, [key]: e.target.value }));
  return <form onSubmit={(e) => { e.preventDefault(); onSubmit(form); }} className="space-y-4">
    <div className="grid gap-4 sm:grid-cols-2">
      <Field label="Doctor ID"><input required className={inputClass} placeholder="e.g. DR-012" value={form.doctor_id} onChange={set("doctor_id")} /></Field>
      <Field label="Full name"><input required className={inputClass} placeholder="Doctor name" value={form.name} onChange={set("name")} /></Field>
      <Field label="Specialization"><input required className={inputClass} placeholder="e.g. Cardiology" value={form.specialization} onChange={set("specialization")} /></Field>
      <Field label="Contact"><input required className={inputClass} placeholder="Fictional contact" value={form.contact} onChange={set("contact")} /></Field>
    </div>
    <div className="flex justify-end border-t border-line pt-4"><Button type="submit" disabled={busy}>{busy ? <LoaderCircle size={15} className="animate-spin" /> : <Plus size={15} />}Add doctor</Button></div>
  </form>;
}

function QueueForm({ patients, onSubmit, busy, initialPatientId = "" }) {
  const [patientId, setPatientId] = useState(initialPatientId);
  const [type, setType] = useState("routine");
  const [urgency, setUrgency] = useState("3");
  return <form onSubmit={(e) => { e.preventDefault(); onSubmit({ patientId, type, urgency: Number(urgency) }); }} className="space-y-5">
    <Field label="Patient"><select required className={inputClass} value={patientId} onChange={(e) => setPatientId(e.target.value)}><option value="">Select a patient</option>{patients.map((p) => <option key={p.patient_id} value={p.patient_id}>{p.patient_id} · {p.name}</option>)}</select></Field>
    <Field label="Queue type"><div className="grid grid-cols-2 gap-2"><button type="button" onClick={() => setType("routine")} className={cx("rounded-xl border p-3 text-left transition", type === "routine" ? "border-teal-500 bg-teal-50" : "border-line hover:bg-canvas")}><div className="mb-2 flex items-center gap-2 text-sm font-bold"><Clock3 size={16} className="text-teal-700" />Routine</div><p className="text-[11px] text-muted">First in, first out</p></button><button type="button" onClick={() => setType("emergency")} className={cx("rounded-xl border p-3 text-left transition", type === "emergency" ? "border-rose-300 bg-rose-50" : "border-line hover:bg-canvas")}><div className="mb-2 flex items-center gap-2 text-sm font-bold"><Siren size={16} className="text-rose-600" />Emergency</div><p className="text-[11px] text-muted">Demo priority score</p></button></div></Field>
    {type === "emergency" && <Field label="Demo urgency score" hint="Higher scores are served first. This is not clinical triage."><div className="grid grid-cols-5 gap-2">{[1,2,3,4,5].map((n) => <button type="button" key={n} onClick={() => setUrgency(String(n))} className={cx("rounded-xl border py-3 text-sm font-bold transition", urgency === String(n) ? "border-rose-400 bg-rose-50 text-rose-600" : "border-line text-muted hover:bg-canvas")}>{n}</button>)}</div></Field>}
    <div className="flex justify-end border-t border-line pt-4"><Button type="submit" disabled={busy || !patientId}>{busy ? <LoaderCircle size={15} className="animate-spin" /> : <Plus size={15} />}Add to queue</Button></div>
  </form>;
}

function AssignForm({ patients, doctors, onSubmit, busy }) {
  const [patientId, setPatientId] = useState("");
  const [specialization, setSpecialization] = useState("");
  const specializations = [...new Set(doctors.map((d) => d.specialization))];
  return <form onSubmit={(e) => { e.preventDefault(); onSubmit({ patient_id: patientId, specialization }); }} className="space-y-4">
    <Field label="Patient"><select required className={inputClass} value={patientId} onChange={(e) => setPatientId(e.target.value)}><option value="">Select patient</option>{patients.map((p) => <option key={p.patient_id} value={p.patient_id}>{p.patient_id} · {p.name}</option>)}</select></Field>
    <Field label="Specialization"><select required className={inputClass} value={specialization} onChange={(e) => setSpecialization(e.target.value)}><option value="">Choose a specialty</option>{specializations.map((s) => <option key={s} value={s}>{s}</option>)}</select></Field>
    <div className="rounded-xl bg-canvas p-3 text-xs leading-5 text-muted">PulseQ selects the available matching doctor with the smallest number of active demo assignments.</div>
    <div className="flex justify-end border-t border-line pt-4"><Button type="submit" disabled={busy || !patientId || !specialization}>{busy ? <LoaderCircle size={15} className="animate-spin" /> : <UserPlus size={15} />}Assign doctor</Button></div>
  </form>;
}

function StatCard({ label, value, detail, icon: Icon, tone = "teal", trend }) {
  const tones = { teal: "bg-teal-50 text-teal-700", amber: "bg-amber-50 text-amber-600", rose: "bg-rose-50 text-rose-600", slate: "bg-slate-100 text-slate-600" };
  return <Panel className="p-5"><div className="flex items-start justify-between"><div className={cx("flex h-10 w-10 items-center justify-center rounded-xl", tones[tone])}><Icon size={19} strokeWidth={1.8} /></div>{trend && <span className="rounded-lg bg-canvas px-2 py-1 text-[10px] font-bold text-muted">{trend}</span>}</div><div className="mt-5"><div className="font-display text-3xl font-extrabold tracking-tight text-ink">{value ?? "—"}</div><div className="mt-1 text-sm font-semibold text-ink">{label}</div><div className="mt-1 text-xs text-muted">{detail}</div></div></Panel>;
}

function PatientTable({ patients, onQueue, onEdit, onDelete, compact = false }) {
  if (!patients.length) return <EmptyState icon={Users} title="No patient records yet" text="Create a synthetic demo patient to start using the dashboard." />;
  return <div className="overflow-x-auto"><table className="w-full min-w-[620px] text-left"><thead><tr className="border-b border-line bg-[#fbfcfa] text-[10px] font-bold uppercase tracking-[0.13em] text-muted"><th className="px-5 py-3.5">Patient</th><th className="px-4 py-3.5">Patient ID</th><th className="px-4 py-3.5">Age</th><th className="px-4 py-3.5">Reason</th><th className="px-5 py-3.5 text-right">Actions</th></tr></thead><tbody>{patients.map((p, index) => <tr key={p.patient_id} className="border-b border-line/80 last:border-0 hover:bg-[#fcfdfb]"><td className="px-5 py-3.5"><div className="flex items-center gap-3"><Avatar name={p.name} size="sm" /><div><div className="text-sm font-bold text-ink">{p.name}</div><div className="mt-0.5 text-[11px] text-muted">{p.sex}</div></div></div></td><td className="px-4 py-3.5"><span className="rounded-lg bg-canvas px-2 py-1 font-mono text-[11px] font-bold text-slate-600">{p.patient_id}</span></td><td className="px-4 py-3.5 text-sm text-slate-600">{p.age}</td><td className="max-w-[180px] truncate px-4 py-3.5 text-sm text-slate-600">{p.reason}</td><td className="px-5 py-3.5"><div className="flex justify-end gap-1"><button title="Add to queue" onClick={() => onQueue(p)} className="rounded-lg p-2 text-muted hover:bg-teal-50 hover:text-teal-700"><ListOrdered size={15} /></button><button title="Edit patient" onClick={() => onEdit(p)} className="rounded-lg p-2 text-muted hover:bg-slate-100 hover:text-ink"><MoreHorizontal size={16} /></button>{!compact && <button title="Delete patient" onClick={() => onDelete(p)} className="rounded-lg p-2 text-muted hover:bg-rose-50 hover:text-rose-600"><X size={15} /></button>}</div></td></tr>)}</tbody></table></div>;
}

function QueueList({ cases = [], kind, onServe, serving }) {
  if (!cases.length) return <EmptyState icon={kind === "emergency" ? Siren : Clock3} title="Queue is clear" text="There are no patients waiting in this queue." />;
  return <div className="divide-y divide-line">{cases.map((item, i) => { const p = kind === "emergency" ? item : item; return <div key={p.patient_id} className="flex items-center gap-3 px-5 py-3.5"><div className={cx("flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-xs font-extrabold", kind === "emergency" ? "bg-rose-50 text-rose-600" : "bg-canvas text-muted")}>{kind === "emergency" ? p.urgency : i + 1}</div><Avatar name={p.name} size="sm" /><div className="min-w-0 flex-1"><div className="truncate text-sm font-bold text-ink">{p.name}</div><div className="mt-0.5 truncate text-[11px] text-muted">{p.patient_id} · {kind === "emergency" ? `Demo urgency ${p.urgency}` : "Routine visit"}</div></div>{kind === "emergency" ? <Status tone={p.urgency >= 4 ? "rose" : p.urgency >= 3 ? "amber" : "neutral"}>{p.urgency >= 4 ? "High demo" : p.urgency >= 3 ? "Medium" : "Standard"}</Status> : <span className="text-[11px] font-medium text-muted">{i === 0 ? "Next" : `#${i + 1}`}</span>}</div>; })}<div className="border-t border-line bg-[#fcfdfb] px-5 py-3"><Button variant="secondary" className="w-full" onClick={onServe} disabled={serving}>{serving ? <LoaderCircle size={14} className="animate-spin" /> : <Check size={14} />}Serve next patient</Button></div></div>;
}

export default function App() {
  const [page, setPage] = useState("Overview");
  const [collapsed, setCollapsed] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);
  const [dashboard, setDashboard] = useState(null);
  const [patients, setPatients] = useState([]);
  const [routine, setRoutine] = useState([]);
  const [emergency, setEmergency] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [serving, setServing] = useState("");
  const [search, setSearch] = useState("");
  const [toast, setToast] = useState(null);
  const [modal, setModal] = useState(null);
  const [editing, setEditing] = useState(null);
  const [sortField, setSortField] = useState("id");
  const [sortAlgorithm, setSortAlgorithm] = useState("merge");
  const [sortOrder, setSortOrder] = useState("asc");
  const [sortCollection, setSortCollection] = useState("patients");
  const [sortResults, setSortResults] = useState(null);
  const [searchMethod, setSearchMethod] = useState("linear");
  const [searchResults, setSearchResults] = useState(null);

  const refresh = useCallback(async (quiet = false) => {
    if (!quiet) setLoading(true);
    try {
      const [dash, patientRows, routineRows, emergencyRows, doctorRows] = await Promise.all([
        api("/dashboard"), api("/patients"), api("/routine"), api("/emergency"), api("/doctors"),
      ]);
      setDashboard(dash); setPatients(patientRows); setRoutine(routineRows); setEmergency(emergencyRows); setDoctors(doctorRows);
    } catch (error) {
      setToast({ type: "error", message: error.message || "Could not connect to PulseQ API." });
    } finally { setLoading(false); }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);
  useEffect(() => { if (!toast) return; const id = window.setTimeout(() => setToast(null), 3600); return () => window.clearTimeout(id); }, [toast]);

  const runAction = async (task, success) => {
    setBusy(true);
    try { await task(); await refresh(true); setToast({ type: "success", message: success }); setModal(null); setEditing(null); }
    catch (error) { setToast({ type: "error", message: error.message }); }
    finally { setBusy(false); }
  };

  const seedDemo = () => runAction(() => api("/demo/seed", { method: "POST" }), "Fictional sample workspace loaded.");
  const createPatient = (data) => runAction(() => api("/patients", { method: "POST", body: JSON.stringify(data) }), "Patient record added.");
  const savePatient = (data) => runAction(() => api(`/patients/${encodeURIComponent(editing.patient_id)}`, { method: "PATCH", body: JSON.stringify(data) }), "Patient record updated.");
  const deletePatient = (p) => { if (window.confirm(`Delete ${p.patient_id} from this demo?`)) runAction(() => api(`/patients/${encodeURIComponent(p.patient_id)}`, { method: "DELETE" }), "Patient record deleted."); };
  const createDoctor = (data) => runAction(() => api("/doctors", { method: "POST", body: JSON.stringify(data) }), "Doctor added to the directory.");
  const addToQueue = ({ patientId, type, urgency }) => runAction(() => type === "routine"
    ? api(`/routine/${encodeURIComponent(patientId)}/enqueue`, { method: "POST" })
    : api(`/emergency/${encodeURIComponent(patientId)}/enqueue`, { method: "POST", body: JSON.stringify({ urgency }) }), type === "routine" ? "Added to the routine queue." : "Added to the emergency queue.");
  const serveNext = (type) => runAction(async () => {
    setServing(type);
    try { const patient = await api(type === "routine" ? "/routine/serve" : "/emergency/serve", { method: "POST" }); setToast({ type: "success", message: `Served next: ${patient.patient_id} · ${patient.name}` }); await refresh(true); }
    finally { setServing(""); }
  }, "Queue updated.");
  const toggleDoctor = (d) => runAction(() => api(`/doctors/${encodeURIComponent(d.doctor_id)}/availability`, { method: "PATCH" }), `${d.name}'s availability updated.`);
  const assignDoctor = (data) => runAction(() => api("/assignments", { method: "POST", body: JSON.stringify(data) }), "Doctor assigned using the least-loaded matching specialist.");
  const releaseDoctor = (p) => runAction(() => api(`/assignments/${encodeURIComponent(p.patient_id)}`, { method: "DELETE" }), "Doctor assignment released.");

  const filteredPatients = useMemo(() => {
    const q = search.trim().toLocaleLowerCase();
    if (!q) return patients;
    return patients.filter((p) => [p.patient_id, p.name, p.reason].some((v) => String(v).toLocaleLowerCase().includes(q)));
  }, [patients, search]);

  const doSearch = async (e) => {
    e?.preventDefault();
    if (!search.trim()) { setSearchResults(null); return; }
    try { setSearchResults(await api(`/search?q=${encodeURIComponent(search.trim())}&method=${searchMethod}`)); }
    catch (error) { setToast({ type: "error", message: error.message }); }
  };
  const doSort = async () => {
    try { const rows = await api(`/sort?collection=${sortCollection}&field=${sortField}&algorithm=${sortAlgorithm}&order=${sortOrder}`); setSortResults(rows); }
    catch (error) { setToast({ type: "error", message: error.message }); }
  };

  const openEdit = (patient) => { setEditing(patient); setModal("editPatient"); };
  const closeModal = () => { setModal(null); setEditing(null); };

  const titleMap = {
    Overview: ["OVERVIEW", "Good work starts with a clear picture.", "A quiet, live view of the demo workflow."],
    Patients: ["PATIENT RECORDS", "Patient directory", "Manage synthetic demo records and their workflow."],
    "Queue desk": ["QUEUE MANAGEMENT", "Queue desk", "Routine flow and emergency priority, side by side."],
    Doctors: ["CARE TEAM", "Doctor directory", "Specialization, availability and active demo assignments."],
    "DSA lab": ["ALGORITHM WORKBENCH", "DSA lab", "Explore the algorithms that power PulseQ."],
  };

  return <div className="min-h-screen bg-canvas text-ink">
    {mobileNav && <button className="fixed inset-0 z-30 bg-ink/30 lg:hidden" onClick={() => setMobileNav(false)} aria-label="Close navigation overlay" />}
    <aside className={cx("fixed inset-y-0 left-0 z-40 flex flex-col border-r border-line bg-white transition-all duration-200", collapsed ? "w-[84px]" : "w-[252px]", mobileNav ? "translate-x-0" : "-translate-x-full lg:translate-x-0")}>
      <div className={cx("flex h-[82px] items-center border-b border-line", collapsed ? "justify-center px-3" : "gap-3 px-6")}>
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[14px] bg-ink text-white"><HeartPulse size={21} strokeWidth={2.2} /></div>
        {!collapsed && <div className="min-w-0"><div className="font-display text-[18px] font-extrabold tracking-tight">pulse<span className="text-teal-600">q</span><span className="ml-1.5 rounded-md bg-canvas px-1.5 py-0.5 align-middle text-[9px] font-bold tracking-wider text-muted">DEMO</span></div><div className="mt-0.5 text-[10px] font-medium text-muted">Care operations</div></div>}
      </div>
      {!collapsed && <div className="px-5 pb-2 pt-6 text-[9px] font-extrabold uppercase tracking-[0.2em] text-slate-400">Workspace</div>}
      <nav className={cx("flex-1 space-y-1 py-2", collapsed ? "px-3" : "px-3.5")}>{navItems.map(({ id, icon: Icon, label, marker }) => <button key={id} onClick={() => { setPage(id); setMobileNav(false); }} title={collapsed ? label : undefined} className={cx("group flex w-full items-center rounded-xl py-3 text-left text-sm font-semibold transition", collapsed ? "justify-center px-2" : "gap-3 px-3.5", page === id ? "bg-teal-50 text-teal-700" : "text-slate-500 hover:bg-canvas hover:text-ink")}><Icon size={18} strokeWidth={page === id ? 2.2 : 1.8} /><span className={cx("flex-1", collapsed && "hidden")}>{label}</span>{marker && !collapsed && <span className="rounded-md bg-white px-1.5 py-0.5 text-[10px] font-bold text-muted">{routine.length + emergency.length}</span>}</button>)}</nav>
      {!collapsed && <div className="mx-4 mb-4 rounded-2xl border border-teal-100 bg-teal-50/70 p-4"><div className="mb-2 flex items-center gap-2 text-teal-700"><ShieldCheck size={16} /><span className="text-xs font-bold">Academic sandbox</span></div><p className="text-[11px] leading-[1.6] text-slate-500">Use fictional records only. No clinical decisions or real patient data.</p><div className="mt-3 flex items-center gap-1.5 text-[10px] font-bold text-teal-700"><span className="h-1.5 w-1.5 rounded-full bg-teal-500" />Local-only storage</div></div>}
      <div className={cx("border-t border-line py-3", collapsed ? "px-3" : "px-4")}><button onClick={() => setCollapsed(!collapsed)} className={cx("flex w-full items-center rounded-xl py-2.5 text-xs font-semibold text-muted hover:bg-canvas", collapsed ? "justify-center" : "gap-2 px-3")}>{collapsed ? <PanelLeftOpen size={16} /> : <><PanelLeftClose size={16} />Collapse sidebar</>}</button></div>
    </aside>

    <div className={cx("min-h-screen transition-[margin] duration-200", collapsed ? "lg:ml-[84px]" : "lg:ml-[252px]")}>
      <header className="sticky top-0 z-20 flex h-[72px] items-center justify-between gap-3 border-b border-line bg-white/90 px-4 backdrop-blur-xl sm:px-7 lg:px-9">
        <div className="flex min-w-0 items-center gap-3"><button className="rounded-lg p-2 text-muted hover:bg-canvas lg:hidden" onClick={() => setMobileNav(true)}><Menu size={19} /></button><div className="hidden items-center gap-2 text-xs text-muted sm:flex"><span>PulseQ</span><ChevronRight size={13} /><span className="font-semibold text-ink">{page}</span></div><div className="sm:hidden font-display text-sm font-extrabold">{page}</div></div>
        <div className="flex items-center gap-2 sm:gap-3"><div className="relative hidden w-[220px] md:block xl:w-[280px]"><Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} /><input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && doSearch()} placeholder="Search patients..." className="w-full rounded-xl border border-line bg-[#fbfcfa] py-2.5 pl-9 pr-10 text-xs outline-none transition focus:border-teal-500 focus:bg-white" /><kbd className="absolute right-3 top-1/2 -translate-y-1/2 rounded border border-line bg-white px-1 py-0.5 text-[9px] text-slate-400">↵</kbd></div><button onClick={() => refresh()} title="Refresh data" className="rounded-xl border border-line bg-white p-2.5 text-muted transition hover:bg-canvas hover:text-ink"><RefreshCw size={15} className={loading ? "animate-spin" : ""} /></button><div className="hidden h-8 w-px bg-line sm:block" /><div className="flex items-center gap-2.5"><Avatar name="PulseQ Operator" /><div className="hidden sm:block"><div className="text-xs font-bold text-ink">Demo operator</div><div className="mt-0.5 text-[10px] text-muted">Local workspace</div></div><ChevronDown size={14} className="hidden text-muted sm:block" /></div></div>
      </header>

      <main className="mx-auto max-w-[1600px] px-4 pb-10 pt-7 sm:px-7 lg:px-9 lg:pt-9">
        {loading && !dashboard ? <div className="flex min-h-[60vh] items-center justify-center"><div className="flex items-center gap-3 text-sm text-muted"><LoaderCircle className="animate-spin text-teal-600" size={19} />Connecting to PulseQ API...</div></div> : !dashboard ? <Panel><EmptyState icon={Activity} title="PulseQ API is not responding" text="Start the FastAPI server, then refresh this page." action={<Button onClick={() => refresh()}><RefreshCw size={15} />Try again</Button>} /></Panel> : <>
          <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><div className="mb-2 flex items-center gap-2 text-[10px] font-extrabold uppercase tracking-[0.2em] text-teal-600"><span className="h-1.5 w-1.5 rounded-full bg-teal-500" />{titleMap[page][0]}</div><h1 className="font-display text-[27px] font-extrabold leading-tight tracking-[-0.04em] text-ink sm:text-[32px]">{titleMap[page][1]}</h1><p className="mt-2 text-sm text-muted">{titleMap[page][2]}</p></div><div className="flex flex-wrap items-center gap-2"><div className="mr-1 hidden items-center gap-2 rounded-xl border border-line bg-white px-3 py-2.5 text-xs font-semibold text-muted md:flex"><CalendarDays size={14} /> Demo environment</div>{patients.length === 0 && doctors.length === 0 && <Button variant="secondary" onClick={seedDemo}><Sparkles size={15} />Load sample data</Button>}{page === "Doctors" ? <Button onClick={() => setModal("newDoctor")}><Plus size={16} />Add doctor</Button> : <Button onClick={() => setModal("newPatient")}><Plus size={16} />New patient</Button>}</div></div>

          {page === "Overview" && <div className="space-y-6">
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <StatCard label="Patient records" value={dashboard.stats.patients} detail="Registered demo patients" icon={Users} tone="teal" trend="DIRECTORY" />
              <StatCard label="Routine waiting" value={dashboard.stats.routine_waiting} detail="First in, first out" icon={Clock3} tone="slate" trend="FIFO" />
              <StatCard label="Emergency queue" value={dashboard.stats.emergency_waiting} detail="Ordered by demo urgency" icon={Siren} tone="rose" trend="MAX-HEAP" />
              <StatCard label="Available doctors" value={dashboard.stats.doctors_available} detail={`of ${dashboard.stats.doctors} in directory`} icon={Stethoscope} tone="amber" trend="CARE TEAM" />
            </div>

            <div className="grid gap-5 xl:grid-cols-[1.12fr_0.88fr]">
              <Panel className="overflow-hidden"><PanelTitle icon={Siren} title="Emergency priority" note="Highest demo urgency served first" action={<button onClick={() => setPage("Queue desk")} className="flex items-center gap-1 text-xs font-bold text-teal-700 hover:text-teal-600">Open queue <ArrowRight size={13} /></button>} /><QueueList cases={emergency.slice(0, 4)} kind="emergency" onServe={() => serveNext("emergency")} serving={serving === "emergency"} /></Panel>
              <Panel className="overflow-hidden"><PanelTitle icon={Clock3} title="Routine queue" note="First in, first out" action={<button onClick={() => setPage("Queue desk")} className="flex items-center gap-1 text-xs font-bold text-teal-700 hover:text-teal-600">Open queue <ArrowRight size={13} /></button>} /><QueueList cases={routine.slice(0, 4)} kind="routine" onServe={() => serveNext("routine")} serving={serving === "routine"} /></Panel>
            </div>

            <div className="grid gap-5 xl:grid-cols-[1.35fr_0.65fr]">
              <Panel className="overflow-hidden"><PanelTitle icon={Users} title="Recent patient records" note="Latest registrations" action={<button onClick={() => setPage("Patients")} className="text-xs font-bold text-teal-700 hover:text-teal-600">View directory <ArrowRight size={13} className="ml-1 inline" /></button>} /><PatientTable patients={dashboard.recent_patients} compact onQueue={(p) => { setEditing(p); setModal("queue"); }} onEdit={openEdit} onDelete={deletePatient} /></Panel>
              <Panel className="overflow-hidden"><PanelTitle icon={Stethoscope} title="Care team" note="Doctor availability overview" action={<button onClick={() => setPage("Doctors")} className="text-xs font-bold text-teal-700">View all <ArrowRight size={13} className="ml-1 inline" /></button>} /><div className="divide-y divide-line">{dashboard.doctors.length ? dashboard.doctors.slice(0, 5).map((d) => <div key={d.doctor_id} className="flex items-center gap-3 px-5 py-3.5"><Avatar name={d.name} size="sm" /><div className="min-w-0 flex-1"><div className="truncate text-sm font-bold text-ink">{d.name}</div><div className="mt-0.5 text-[11px] text-muted">{d.specialization} · {d.current_load} active</div></div><Status tone={d.available ? "teal" : "neutral"}>{d.available ? "Available" : "Away"}</Status></div>) : <EmptyState icon={Stethoscope} title="No doctors yet" text="Add a doctor to enable assignment demos." />}</div></Panel>
            </div>
            <div className="flex items-start gap-3 rounded-2xl border border-amber-100 bg-amber-50/60 px-4 py-3.5"><ShieldCheck size={17} className="mt-0.5 shrink-0 text-amber-600" /><div><p className="text-xs font-bold text-ink">A note on the demo</p><p className="mt-1 text-xs leading-5 text-slate-600">PulseQ is an academic DSA prototype. Urgency values are illustrative only, records are stored in memory, and this interface must not be used for real patient care.</p></div></div>
          </div>}

          {page === "Patients" && <div className="space-y-5"><div className="grid gap-4 sm:grid-cols-3"><StatCard label="All records" value={patients.length} detail="In-memory directory" icon={Users} tone="teal" /><StatCard label="Waiting in queues" value={routine.length + emergency.length} detail="Routine + emergency" icon={ListOrdered} tone="amber" /><StatCard label="Searchable records" value={filteredPatients.length} detail={search ? "Matches current filter" : "No active filter"} icon={Search} tone="slate" /></div><Panel className="overflow-hidden"><div className="flex flex-col gap-3 border-b border-line px-5 py-4 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="text-sm font-bold">Patient directory</h2><p className="mt-1 text-xs text-muted">Records are stored in the custom linked list.</p></div><div className="flex gap-2"><div className="relative flex-1 sm:w-64"><Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input className={cx(inputClass, "py-2 pl-9")} placeholder="Filter ID, name, reason..." value={search} onChange={(e) => { setSearch(e.target.value); setSearchResults(null); }} /></div><Button variant="secondary" onClick={() => setModal("newPatient")}><Plus size={15} />Add</Button></div></div><PatientTable patients={filteredPatients} onQueue={(p) => { setEditing(p); setModal("queue"); }} onEdit={openEdit} onDelete={deletePatient} /></Panel></div>}

          {page === "Queue desk" && <div className="space-y-5"><div className="grid gap-4 sm:grid-cols-3"><StatCard label="Total waiting" value={routine.length + emergency.length} detail="Across both queues" icon={Users} tone="slate" /><StatCard label="Routine FIFO" value={routine.length} detail="First arrival served first" icon={Clock3} tone="teal" /><StatCard label="Emergency heap" value={emergency.length} detail="Priority, then arrival order" icon={Siren} tone="rose" /></div><div className="grid gap-5 xl:grid-cols-2"><Panel className="overflow-hidden"><PanelTitle icon={Clock3} title="Routine queue" note="Linked FIFO · O(1) enqueue and dequeue" action={<Button variant="secondary" className="px-3 py-2" onClick={() => setModal("queue")}><Plus size={14} />Add</Button>} /><QueueList cases={routine} kind="routine" onServe={() => serveNext("routine")} serving={serving === "routine"} /></Panel><Panel className="overflow-hidden"><PanelTitle icon={Siren} title="Emergency priority queue" note="Binary max-heap · O(log n) enqueue and dequeue" action={<Button variant="secondary" className="px-3 py-2" onClick={() => setModal("queue")}><Plus size={14} />Add</Button>} /><QueueList cases={emergency} kind="emergency" onServe={() => serveNext("emergency")} serving={serving === "emergency"} /></Panel></div><div className="rounded-2xl border border-rose-100 bg-rose-50/50 p-4 text-xs leading-5 text-slate-600"><span className="font-bold text-rose-600">Urgency disclaimer.</span> Scores from 1 to 5 are used only to demonstrate heap ordering. They are not clinical triage levels, medical advice, or a basis for real care decisions.</div></div>}

          {page === "Doctors" && <div className="space-y-5"><div className="grid gap-4 sm:grid-cols-3"><StatCard label="Doctors listed" value={doctors.length} detail="Directory size" icon={Stethoscope} tone="teal" /><StatCard label="Available now" value={doctors.filter((d) => d.available).length} detail="Can receive new demo assignments" icon={CircleCheck} tone="slate" /><StatCard label="Active assignments" value={doctors.reduce((n, d) => n + d.current_load, 0)} detail="Current demo load" icon={ClipboardList} tone="amber" /></div><Panel className="overflow-hidden"><PanelTitle icon={Stethoscope} title="Doctor directory" note="Allocation selects the least-loaded available matching specialty" action={<Button onClick={() => setModal("newDoctor")}><Plus size={15} />Add doctor</Button>} />{doctors.length ? <div className="overflow-x-auto"><table className="w-full min-w-[640px] text-left"><thead><tr className="border-b border-line bg-[#fbfcfa] text-[10px] font-bold uppercase tracking-[0.13em] text-muted"><th className="px-5 py-3.5">Doctor</th><th className="px-4 py-3.5">Specialization</th><th className="px-4 py-3.5">Active load</th><th className="px-4 py-3.5">Status</th><th className="px-5 py-3.5 text-right">Action</th></tr></thead><tbody>{doctors.map((d) => <tr key={d.doctor_id} className="border-b border-line/80 last:border-0"><td className="px-5 py-4"><div className="flex items-center gap-3"><Avatar name={d.name} /><div><div className="text-sm font-bold">{d.name}</div><div className="mt-0.5 font-mono text-[11px] text-muted">{d.doctor_id}</div></div></div></td><td className="px-4 py-4 text-sm text-slate-600">{d.specialization}</td><td className="px-4 py-4"><span className="rounded-lg bg-canvas px-2.5 py-1.5 text-xs font-bold">{d.current_load}</span></td><td className="px-4 py-4"><Status tone={d.available ? "teal" : "neutral"}>{d.available ? "Available" : "Unavailable"}</Status></td><td className="px-5 py-4 text-right"><Button variant="secondary" className="px-3 py-2 text-xs" onClick={() => toggleDoctor(d)}>{d.available ? "Set unavailable" : "Set available"}</Button></td></tr>)}</tbody></table></div> : <EmptyState icon={Stethoscope} title="Your directory is empty" text="Add a few fictional doctors to demonstrate specialty matching and load-aware assignment." action={<Button onClick={() => setModal("newDoctor")}><Plus size={15} />Add doctor</Button>} />}</Panel><Panel className="overflow-hidden"><PanelTitle icon={UserPlus} title="Specialization assignment" note="Uses PulseQ's DoctorDirectory allocation logic" action={<Button variant="secondary" onClick={() => setModal("assign")}><UserPlus size={15} />Assign patient</Button>} /><div className="p-5"><div className="grid gap-3 sm:grid-cols-3">{[{label:"Matching specialty",text:"Only doctors with the requested specialization are considered."},{label:"Availability first",text:"Unavailable doctors are skipped for new assignments."},{label:"Least-loaded wins",text:"The doctor with fewer active assignments is selected."}].map((x) => <div key={x.label} className="rounded-xl bg-canvas p-4"><div className="mb-2 text-xs font-bold">{x.label}</div><p className="text-xs leading-5 text-muted">{x.text}</p></div>)}</div></div></Panel></div>}

          {page === "DSA lab" && <div className="space-y-5"><div className="grid gap-4 md:grid-cols-2"><Panel className="p-5"><div className="mb-4 flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal-700"><Search size={18} /></div><div><h2 className="text-sm font-bold">Manual search</h2><p className="mt-1 text-xs text-muted">Try the implemented search functions.</p></div></div><form onSubmit={doSearch} className="space-y-3"><Field label="Search query"><input value={search} onChange={(e) => setSearch(e.target.value)} className={inputClass} placeholder="Patient ID or part of a name" required /></Field><Field label="Algorithm"><select value={searchMethod} onChange={(e) => setSearchMethod(e.target.value)} className={inputClass}><option value="linear">Linear search by ID · O(n)</option><option value="name">Partial name search · O(n)</option><option value="binary">Binary search by ID · O(log n)</option></select></Field><Button type="submit" className="w-full"><Search size={15} />Run search</Button></form>{searchResults && <div className="mt-4 rounded-xl border border-line"><div className="border-b border-line px-3 py-2 text-xs font-bold">{searchResults.length} result{searchResults.length === 1 ? "" : "s"}</div>{searchResults.length ? searchResults.map((p) => <div key={p.patient_id} className="flex items-center gap-3 px-3 py-3"><Avatar name={p.name} size="sm" /><div><div className="text-xs font-bold">{p.name}</div><div className="mt-0.5 text-[11px] text-muted">{p.patient_id} · Age {p.age}</div></div></div>) : <p className="p-3 text-xs text-muted">No match found.</p>}</div>}</Panel><Panel className="p-5"><div className="mb-4 flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600"><ArrowUpDown size={18} /></div><div><h2 className="text-sm font-bold">Manual sorting</h2><p className="mt-1 text-xs text-muted">Sort a snapshot without changing live storage.</p></div></div><div className="space-y-3"><Field label="Collection"><select className={inputClass} value={sortCollection} onChange={(e) => { setSortCollection(e.target.value); setSortField(e.target.value === "patients" ? "id" : "urgency"); setSortResults(null); }}><option value="patients">Patient records</option><option value="emergency">Emergency cases</option></select></Field><Field label="Sort field"><select className={inputClass} value={sortField} onChange={(e) => setSortField(e.target.value)}>{(sortCollection === "patients" ? [{v:"id",t:"Patient ID"},{v:"name",t:"Patient name"},{v:"age",t:"Patient age"}] : [{v:"urgency",t:"Demo urgency"},{v:"arrival",t:"Arrival order"}]).map((x) => <option key={x.v} value={x.v}>{x.t}</option>)}</select></Field><div className="grid grid-cols-2 gap-3"><Field label="Algorithm"><select className={inputClass} value={sortAlgorithm} onChange={(e) => setSortAlgorithm(e.target.value)}><option value="merge">Merge sort</option><option value="insertion">Insertion sort</option></select></Field><Field label="Order"><select className={inputClass} value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}><option value="asc">Ascending</option><option value="desc">Descending</option></select></Field></div><Button className="w-full" onClick={doSort}><ArrowUpDown size={15} />Run sort</Button></div></Panel></div><Panel className="overflow-hidden"><PanelTitle icon={Activity} title="Algorithm output" note={sortResults ? `${sortResults.length} records · ${sortAlgorithm === "merge" ? "Merge sort" : "Insertion sort"}` : "Run a search or sort to inspect results"} />{sortResults ? (sortResults.length ? <div className="overflow-x-auto"><table className="w-full text-left"><thead><tr className="border-b border-line bg-[#fbfcfa] text-[10px] font-bold uppercase tracking-wider text-muted"><th className="px-5 py-3">Position</th><th className="px-5 py-3">Record</th><th className="px-5 py-3">Key value</th><th className="px-5 py-3">Details</th></tr></thead><tbody>{sortResults.map((r, i) => <tr key={r.patient_id} className="border-b border-line last:border-0"><td className="px-5 py-3 text-xs text-muted">{String(i + 1).padStart(2, "0")}</td><td className="px-5 py-3 text-sm font-bold">{r.name}<div className="mt-0.5 font-mono text-[10px] text-muted">{r.patient_id}</div></td><td className="px-5 py-3 text-sm">{sortField === "age" ? r.age : sortField === "name" ? r.name : sortField === "urgency" ? r.urgency : sortField === "arrival" ? r.arrival_order : r.patient_id}</td><td className="px-5 py-3 text-xs text-muted">{r.reason || `Demo urgency ${r.urgency ?? "—"}`}</td></tr>)}</tbody></table></div> : <EmptyState title="No records to sort" text="Add records or queue cases, then run the sort again." />) : <EmptyState icon={Sparkles} title="Your results will appear here" text="Choose an algorithm above. Sorting always works on a copy, leaving the live DSA structures unchanged." />}</Panel><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{[{name:"Singly linked list",complexity:"O(n) lookup",note:"Patient record store",icon:Users},{name:"FIFO queue",complexity:"O(1) enqueue",note:"Routine appointments",icon:Clock3},{name:"Binary max-heap",complexity:"O(log n) insert",note:"Emergency priority",icon:Zap},{name:"Merge sort",complexity:"O(n log n)",note:"Stable comparison sort",icon:ArrowUpDown}].map((x) => <Panel key={x.name} className="p-4"><x.icon size={17} className="mb-3 text-teal-700" /><div className="text-sm font-bold">{x.name}</div><div className="mt-1 text-xs font-bold text-teal-700">{x.complexity}</div><div className="mt-1 text-[11px] text-muted">{x.note}</div></Panel>)}</div></div>}
        </>}
      </main>
      <footer className="flex flex-col gap-2 border-t border-line px-4 py-4 text-[10px] text-muted sm:flex-row sm:items-center sm:justify-between sm:px-7 lg:px-9"><div className="flex items-center gap-2"><HeartPulse size={13} className="text-teal-600" /><span>PulseQ <span className="text-slate-300">/</span> Academic prototype</span></div><div className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-teal-500" />API connected · In-memory data · Synthetic records only</div></footer>
    </div>

    {modal === "newPatient" && <Modal title="Add a patient" subtitle="Create a fictional record in the linked-list directory." onClose={closeModal}><PatientForm onSubmit={createPatient} busy={busy} /></Modal>}
    {modal === "editPatient" && editing && <Modal title="Edit patient record" subtitle={`Update ${editing.patient_id}. The ID stays immutable.`} onClose={closeModal}><PatientForm key={editing.patient_id} initial={editing} onSubmit={savePatient} busy={busy} /></Modal>}
    {modal === "newDoctor" && <Modal title="Add a doctor" subtitle="Use fictional details for this academic demo." onClose={closeModal}><DoctorForm onSubmit={createDoctor} busy={busy} /></Modal>}
    {modal === "queue" && <Modal title="Add to a queue" subtitle="Choose routine FIFO or emergency demo priority." onClose={closeModal}><QueueForm key={editing?.patient_id || "queue"} initialPatientId={editing?.patient_id || ""} patients={patients} onSubmit={addToQueue} busy={busy} /></Modal>}
    {modal === "assign" && <Modal title="Assign a doctor" subtitle="Match a patient to an available specialty." onClose={closeModal}><AssignForm patients={patients} doctors={doctors} onSubmit={assignDoctor} busy={busy} /></Modal>}

    {toast && <div role="status" className={cx("fixed bottom-5 right-5 z-[70] flex max-w-[min(92vw,420px)] items-start gap-3 rounded-2xl border bg-white px-4 py-3.5 shadow-xl", toast.type === "error" ? "border-rose-100" : "border-teal-100")}><div className={cx("mt-0.5", toast.type === "error" ? "text-rose-600" : "text-teal-600")}>{toast.type === "error" ? <AlertCircle size={17} /> : <CircleCheck size={17} />}</div><p className="flex-1 text-sm font-medium leading-5 text-ink">{toast.message}</p><button onClick={() => setToast(null)} className="text-muted hover:text-ink"><X size={15} /></button></div>}
  </div>;
}
