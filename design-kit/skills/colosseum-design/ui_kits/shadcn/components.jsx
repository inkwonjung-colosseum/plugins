/* global React */
const { useState } = React;

const Icon = ({ name, size = 18, style }) => (
  <span className="mi" style={{ fontSize: size, ...style }}>{name}</span>
);

// ---------- Button ----------
function Button({ variant = 'primary', size = 'md', icon, iconOnly, children, ...rest }) {
  const cls = ['btn', `btn-${size}`, `btn-${variant}`, iconOnly && 'btn-icon'].filter(Boolean).join(' ');
  return (
    <button className={cls} {...rest}>
      {icon && <Icon name={icon} size={16} />}
      {!iconOnly && children}
    </button>
  );
}

// ---------- Field ----------
function Field({ label, required, helper, error, children }) {
  return (
    <div className="field">
      {label && <label className={'field-label ' + (required ? 'required' : '')}>{label}</label>}
      {children}
      {(helper || error) && <div className={'field-helper ' + (error ? 'error' : '')}>{error || helper}</div>}
    </div>
  );
}

function Input({ error, ...rest }) { return <input className={'input ' + (error ? 'error' : '')} {...rest} />; }
function Textarea({ error, ...rest }) { return <textarea className={'textarea ' + (error ? 'error' : '')} {...rest} />; }

// ---------- Select ----------
function Select({ value, onChange, options = [], placeholder = '선택하세요', disabled }) {
  const [open, setOpen] = useState(false);
  const current = options.find(o => o.value === value);
  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <button className="select-trigger" style={{ justifyContent: 'space-between', cursor: disabled ? 'not-allowed' : 'pointer' }}
        onClick={() => !disabled && setOpen(o => !o)} disabled={disabled} type="button">
        <span style={{ color: current ? 'var(--gray-700)' : 'var(--gray-400)' }}>{current?.label || placeholder}</span>
        <Icon name="expand_more" size={18} style={{ color: 'var(--gray-500)' }} />
      </button>
      {open && (
        <>
          <div style={{ position: 'fixed', inset: 0, zIndex: 40 }} onClick={() => setOpen(false)} />
          <div className="popover" style={{ position: 'absolute', top: 'calc(100% + 4px)', left: 0, right: 0, zIndex: 41 }}>
            {options.map(o => (
              <div key={o.value} className="popover-item" onClick={() => { onChange?.(o.value); setOpen(false); }}>
                <span style={{ flex: 1 }}>{o.label}</span>
                {o.value === value && <Icon name="check" size={16} style={{ color: 'var(--clblue-500)' }} />}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

// ---------- Checkbox / Radio / Switch ----------
function Checkbox({ label, ...rest }) { return (<label className="control-row"><input type="checkbox" className="checkbox" {...rest} />{label}</label>); }
function Radio({ label, ...rest }) { return (<label className="control-row"><input type="radio" className="radio" {...rest} />{label}</label>); }
function Switch({ checked, onChange, label }) {
  return (<label className="control-row"><button type="button" className={'switch ' + (checked ? 'on' : '')} onClick={() => onChange?.(!checked)} aria-pressed={checked} />{label}</label>);
}

// ---------- Badge ----------
function Badge({ variant = 'neutral', children, dot }) {
  return (<span className={'badge badge-' + variant}>{dot && <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'currentColor' }} />}{children}</span>);
}

// ---------- Card ----------
function Card({ title, description, children, footer }) {
  return (
    <div className="card">
      {(title || description) && <div className="card-header"><div className="card-title">{title}</div>{description && <div className="card-description">{description}</div>}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// ---------- Tabs ----------
function Tabs({ tabs, value, onChange, variant = 'pill' }) {
  if (variant === 'underline') {
    return (
      <div className="tabs-underline">
        {tabs.map(t => <button key={t.value} className={'tab-underline ' + (t.value === value ? 'active' : '')} onClick={() => onChange(t.value)}>{t.label}</button>)}
      </div>
    );
  }
  return (
    <div className="tabs-list">
      {tabs.map(t => <button key={t.value} className={'tab-trigger ' + (t.value === value ? 'active' : '')} onClick={() => onChange(t.value)}>{t.label}</button>)}
    </div>
  );
}

// ---------- Alert ----------
function Alert({ variant = 'info', title, children }) {
  const iconMap = { info: 'info', success: 'check_circle', warning: 'warning', danger: 'error' };
  const colorMap = { info: 'var(--sky-400)', success: 'var(--green-500)', warning: 'var(--yellow-500)', danger: 'var(--red-500)' };
  return (
    <div className={'alert alert-' + variant}>
      <Icon name={iconMap[variant]} size={18} style={{ color: colorMap[variant], flexShrink: 0, marginTop: 1 }} />
      <div style={{ flex: 1 }}>{title && <div className="alert-title">{title}</div>}<div>{children}</div></div>
    </div>
  );
}

// ---------- Progress ----------
function Progress({ value = 0 }) { return (<div className="progress"><div className="progress-bar" style={{ width: value + '%' }} /></div>); }

// ---------- Avatar ----------
function Avatar({ src, initials, size = 'md' }) {
  const cls = 'avatar ' + (size === 'lg' ? 'avatar-lg' : size === 'sm' ? 'avatar-sm' : '');
  return <div className={cls}>{src ? <img src={src} alt="" /> : initials}</div>;
}

// ---------- Skeleton ----------
function Skeleton({ width = '100%', height = 12, style }) { return <div className="skeleton" style={{ width, height, ...style }} />; }

// ---------- Tooltip ----------
function Tooltip({ content, children }) { return (<span className="tooltip-trigger">{children}<span className="tooltip-content">{content}</span></span>); }

// ---------- Dropdown ----------
function Dropdown({ trigger, items }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <span onClick={() => setOpen(o => !o)}>{trigger}</span>
      {open && (
        <>
          <div style={{ position: 'fixed', inset: 0, zIndex: 40 }} onClick={() => setOpen(false)} />
          <div className="popover" style={{ position: 'absolute', top: 'calc(100% + 4px)', right: 0, zIndex: 41 }}>
            {items.map((it, i) => it.separator ? <div key={i} className="popover-separator" /> :
              <div key={i} className={'popover-item ' + (it.danger ? 'danger' : '')} onClick={() => { it.onClick?.(); setOpen(false); }}>
                {it.icon && <Icon name={it.icon} size={16} />}{it.label}
              </div>)}
          </div>
        </>
      )}
    </div>
  );
}

// ---------- Dialog ----------
function Dialog({ open, onClose, title, description, children, footer }) {
  if (!open) return null;
  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog" onClick={e => e.stopPropagation()}>
        <div className="dialog-header"><div className="dialog-title">{title}</div>{description && <div className="dialog-description">{description}</div>}</div>
        {children && <div className="dialog-body">{children}</div>}
        {footer && <div className="dialog-footer">{footer}</div>}
      </div>
    </div>
  );
}

// ---------- Toast ----------
function Toast({ variant = 'info', title, description, onClose }) {
  const iconMap = { success: 'check_circle', danger: 'error', info: 'info', warning: 'warning' };
  const colorMap = { success: 'var(--green-500)', danger: 'var(--red-500)', info: 'var(--clblue-500)', warning: 'var(--yellow-500)' };
  return (
    <div className={'toast toast-' + variant}>
      <Icon name={iconMap[variant]} size={18} style={{ color: colorMap[variant], marginTop: 1 }} />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--natural-700)' }}>{title}</div>
        {description && <div style={{ fontSize: 12, color: 'var(--gray-500)', marginTop: 2 }}>{description}</div>}
      </div>
      {onClose && <button className="btn btn-ghost btn-xs btn-icon" onClick={onClose}><Icon name="close" size={14} /></button>}
    </div>
  );
}

// ---------- Table ----------
function Table({ columns, rows }) {
  return (
    <div className="table-wrapper">
      <table className="table">
        <thead><tr>{columns.map(c => <th key={c.key} style={{ width: c.width, textAlign: c.align }}>{c.label}</th>)}</tr></thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>{columns.map(c => <td key={c.key} style={{ textAlign: c.align }}>{c.render ? c.render(r) : r[c.key]}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ---------- Breadcrumb ----------
function Breadcrumb({ items }) {
  return (
    <nav className="breadcrumb">
      {items.map((it, i) => (
        <React.Fragment key={i}>
          {i > 0 && <span className="separator-slash">/</span>}
          {i === items.length - 1 ? <span className="current">{it.label}</span> : <a href={it.href || '#'}>{it.label}</a>}
        </React.Fragment>
      ))}
    </nav>
  );
}

// ---------- Pagination ----------
function Pagination({ page, total, onChange }) {
  const pages = Array.from({ length: total }, (_, i) => i + 1);
  return (
    <div className="pagination">
      <button onClick={() => onChange(page - 1)} disabled={page === 1}><Icon name="chevron_left" size={16} /></button>
      {pages.map(p => <button key={p} className={p === page ? 'active' : ''} onClick={() => onChange(p)}>{p}</button>)}
      <button onClick={() => onChange(page + 1)} disabled={page === total}><Icon name="chevron_right" size={16} /></button>
    </div>
  );
}

Object.assign(window, {
  Icon, Button, Field, Input, Textarea, Select, Checkbox, Radio, Switch,
  Badge, Card, Tabs, Alert, Progress, Avatar, Skeleton, Tooltip, Dropdown,
  Dialog, Toast, Table, Breadcrumb, Pagination
});
