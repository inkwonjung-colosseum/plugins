// Tag — status chip
const TAG_VARIANTS = {
  new: { bg: '#D6ECFF', fg: '#005BF6', label: '신규' },
  processing: { bg: '#e5f3ff', fg: '#1a95ff', label: '처리중' },
  waiting: { bg: '#fff1cc', fg: '#a87900', label: '출고대기' },
  shipped: { bg: '#dff7e2', fg: '#289a3a', label: '출고완료' },
  transit: { bg: '#e5f3ff', fg: '#1a95ff', label: '배송중' },
  done: { bg: '#dff7e2', fg: '#289a3a', label: '배송완료' },
  returning: { bg: '#fef3eb', fg: '#f86702', label: '반품요청' },
  cancel: { bg: '#fff0f0', fg: '#f94949', label: '취소' },
  lowStock: { bg: '#fff1cc', fg: '#a87900', label: '부족' },
  outOfStock: { bg: '#fff0f0', fg: '#f94949', label: '품절' },
  normal: { bg: '#dff7e2', fg: '#289a3a', label: '정상' },
};
const Tag = ({ variant = 'new', children }) => {
  const v = TAG_VARIANTS[variant] || TAG_VARIANTS.new;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', height: 22, padding: '0 8px',
      borderRadius: 2, background: v.bg, color: v.fg,
      font: '500 12px var(--font-sans)', whiteSpace: 'nowrap',
    }}>{children || v.label}</span>
  );
};
window.Tag = Tag;

// Button — reusable
const Button = ({ variant='primary', size='sm', children, onClick, icon, disabled }) => {
  const sizeStyle = {
    xs: { height: 24, padding: '0 8px', fontSize: 12, iconSize: 16 },
    sm: { height: 32, padding: '0 12px', fontSize: 14, iconSize: 18 },
    md: { height: 40, padding: '0 16px', fontSize: 14, iconSize: 20 },
  }[size];
  const variantStyle = {
    primary: { background: disabled ? '#F2F2F2' : '#005BF6', color: disabled ? '#929292' : '#fff', border: 'none', fontWeight: 700 },
    outline: { background: '#fff', color: '#464646', border: '1px solid #CACACA', fontWeight: 500 },
    secondary: { background: 'rgba(0,0,0,0.04)', color: '#464646', border: 'none', fontWeight: 500 },
    text: { background: 'transparent', color: '#464646', border: 'none', fontWeight: 500 },
    danger: { background: '#fff', color: '#f94949', border: '1px solid #f94949', fontWeight: 700 },
  }[variant];
  return (
    <button onClick={onClick} disabled={disabled} style={{
      display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 6,
      height: sizeStyle.height, padding: sizeStyle.padding, borderRadius: 6,
      fontFamily: 'var(--font-sans)', fontSize: sizeStyle.fontSize,
      cursor: disabled ? 'not-allowed' : 'pointer',
      ...variantStyle,
    }}>
      {icon && <span className="material-symbols-outlined" style={{ fontSize: sizeStyle.iconSize }}>{icon}</span>}
      {children}
    </button>
  );
};
window.Button = Button;

// FilterBar — search + filter chips
const FilterBar = ({ query, onQueryChange, filters, onFilter, onSearch, onReset }) => (
  <div style={{ background: '#fff', border: '1px solid #e7eaef', borderRadius: 8, padding: 14, display: 'flex', flexDirection: 'column', gap: 12 }}>
    <div style={{ display: 'grid', gridTemplateColumns: '140px 1fr 140px 140px', gap: 10 }}>
      <select style={{ height: 32, padding: '0 10px', border: '1px solid #CACACA', borderRadius: 4, fontSize: 13, color: '#464646', background: '#fff' }}>
        <option>주문번호</option><option>SKU</option><option>고객명</option>
      </select>
      <input value={query} onChange={e => onQueryChange(e.target.value)}
        placeholder="검색 조건을 입력하세요"
        style={{ height: 32, padding: '0 12px', border: '1px solid #CACACA', borderRadius: 4, fontSize: 14, color: '#464646', background: '#fff' }}/>
      <input type="date" style={{ height: 32, padding: '0 10px', border: '1px solid #CACACA', borderRadius: 4, fontSize: 13, color: '#464646', background: '#fff' }}/>
      <input type="date" style={{ height: 32, padding: '0 10px', border: '1px solid #CACACA', borderRadius: 4, fontSize: 13, color: '#464646', background: '#fff' }}/>
    </div>
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      {['전체','신규','처리중','출고대기','출고완료','반품요청','취소'].map((f, i) => (
        <button key={f} onClick={() => onFilter(f)}
          style={{
            height: 28, padding: '0 12px', borderRadius: 4,
            border: filters === f ? '1px solid #005BF6' : '1px solid #CACACA',
            background: filters === f ? '#D6ECFF' : '#fff',
            color: filters === f ? '#005BF6' : '#464646',
            fontWeight: filters === f ? 700 : 500, fontSize: 13, cursor: 'pointer',
          }}>{f}</button>
      ))}
      <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
        <Button variant="outline" size="sm" icon="refresh" onClick={onReset}>초기화</Button>
        <Button variant="primary" size="sm" icon="search" onClick={onSearch}>검색</Button>
      </div>
    </div>
  </div>
);
window.FilterBar = FilterBar;
