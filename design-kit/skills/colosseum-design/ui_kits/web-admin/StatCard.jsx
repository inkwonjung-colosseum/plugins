// StatCard — KPI block for the dashboard
const StatCard = ({ label, value, unit, delta, deltaType = 'up', icon, tone = 'default' }) => {
  const toneColor = {
    default: '#005BF6',
    warning: '#ffbb0e',
    danger: '#f94949',
    safe: '#33c249',
  }[tone];
  return (
    <div style={{
      background: '#fff', border: '1px solid #CACACA', borderRadius: 8,
      padding: 18, display: 'flex', flexDirection: 'column', gap: 12,
      boxShadow: '0 1px 3px 0 rgba(0,0,0,0.06)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontSize: 13, color: '#767676', fontWeight: 500 }}>{label}</div>
        <div style={{
          width: 32, height: 32, borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: tone === 'default' ? '#D6ECFF' : tone === 'warning' ? '#fff1cc' : tone === 'danger' ? '#fff0f0' : '#dff7e2',
        }}>
          <span className="material-symbols-outlined" style={{ fontSize: 18, color: toneColor }}>{icon}</span>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
        <div style={{ fontSize: 28, fontWeight: 700, color: '#29313d', lineHeight: 1.1, fontVariantNumeric: 'tabular-nums' }}>{value}</div>
        {unit && <div style={{ fontSize: 14, color: '#767676', fontWeight: 500 }}>{unit}</div>}
      </div>
      {delta && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: deltaType === 'up' ? '#289a3a' : '#f94949' }}>
          <span className="material-symbols-outlined" style={{ fontSize: 14 }}>
            {deltaType === 'up' ? 'arrow_upward' : 'arrow_downward'}
          </span>
          <span>{delta}</span>
          <span style={{ color: '#767676' }}>vs. 지난 주</span>
        </div>
      )}
    </div>
  );
};

window.StatCard = StatCard;
