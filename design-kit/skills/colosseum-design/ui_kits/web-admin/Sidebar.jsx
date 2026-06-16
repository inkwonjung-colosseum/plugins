// Sidebar (LNB) — Colosseum CDS 2.0 · shadcn-based
// Structure: [logo+WMS badge] [user + bell] [center selector] [search] [admin chip] [scroll nav] [collapse footer]
const { useState } = React;

const NAV_DATA = [
  { group: '주문 · 출고', items: [
    { id: 'orders', icon: 'description', label: '주문 관리', children: [
      { id: 'orders-list', label: '주문 목록' },
      { id: 'orders-new', label: '신규 주문' },
      { id: 'orders-bulk', label: '일괄 등록' },
    ]},
    { id: 'outbound', icon: 'outbox', label: '출고 관리', children: [
      { id: 'outbound-waiting', label: '출고 대기' },
      { id: 'outbound-picking', label: '피킹' },
      { id: 'outbound-packing', label: '패킹' },
      { id: 'outbound-done', label: '출고 완료' },
    ]},
    { id: 'returns', icon: 'assignment_return', label: '반품 관리', children: [
      { id: 'returns-list', label: '반품 목록' },
      { id: 'returns-inspect', label: '반품 검수' },
    ]},
  ]},
  { group: '입고 · 재고', items: [
    { id: 'inbound', icon: 'move_to_inbox', label: '입고 관리', children: [
      { id: 'inbound-plan', label: '입고 예정' },
      { id: 'inbound-receive', label: '입고 접수' },
    ]},
    { id: 'inventory', icon: 'inventory_2', label: '재고 현황', children: [
      { id: 'inventory-stock', label: '재고 조회' },
      { id: 'inventory-move', label: '재고 이동' },
    ]},
  ]},
];

// Color tokens (from Figma pixel-sampled + Colosseum DS)
const C = {
  clblue500: '#005BF6',
  clblue600: '#044ECE',
  clblueSubtle: '#D6ECFF',   // 1-depth hover bg
  sky50: '#E5F3FF',          // 2-depth hover bg
  text: '#29313d',
  textMuted: '#767676',
  textSubtle: '#929292',
  border: '#E7EAEF',
  borderStrong: '#CACACA',
  bg: '#F6F7F9',             // LNB surface
  dark: '#363637',           // center-selector dark card (Figma-specific)
  guideLine: '#E7EAEF',
  dangerRed: '#F94949',
  inputBorder: '#E0E0E2',
};

// —————————————————————————————————————————————
// Leaf (2-depth item) — per Figma: left guide line, left border indicator on selected
const LeafItem = ({ item, active, onClick }) => {
  const [hover, setHover] = useState(false);
  return (
    <div style={{ position: 'relative', display: 'flex', alignItems: 'stretch' }}>
      {/* Left guide line */}
      <div style={{ width: 1, background: C.guideLine, marginLeft: 16, flexShrink: 0 }}/>
      {/* Left selected indicator (absolute, over guide line) */}
      {active && <div style={{
        position: 'absolute', left: 15, top: 4, bottom: 4, width: 3,
        background: C.clblue500, borderRadius: 2,
      }}/>}
      <button
        onClick={onClick}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          flex: 1, height: 32, marginLeft: 8, marginRight: 8, padding: '0 12px',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8,
          borderRadius: 6, border: 'none', cursor: 'pointer', textAlign: 'left',
          background: active ? C.clblue500 : (hover ? C.sky50 : 'transparent'),
          color: active ? '#fff' : (hover ? C.clblue500 : C.text),
          font: `${active ? 700 : 500} 14px var(--font-sans)`,
          transition: 'background 250ms cubic-bezier(0.22, 1, 0.36, 1), color 250ms cubic-bezier(0.22, 1, 0.36, 1)',
        }}>
        <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.label}</span>
        {hover && !active && (
          <span className="material-symbols-outlined" style={{
            fontSize: 16, color: C.clblue500,
            width: 22, height: 22, display: 'inline-flex',
            alignItems: 'center', justifyContent: 'center',
            background: '#fff', borderRadius: 4, border: `1px solid ${C.clblueSubtle}`,
          }}>open_in_new</span>
        )}
      </button>
    </div>
  );
};

// 1-depth group item — Figma: icon + title + chevron, collapsible
const GroupItem = ({ item, activeLeaf, onLeafClick }) => {
  const [open, setOpen] = useState(true);
  const [hover, setHover] = useState(false);
  const hasActiveChild = item.children?.some(c => c.id === activeLeaf);

  return (
    <div style={{ marginBottom: 2 }}>
      <button
        onClick={() => setOpen(!open)}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          width: '100%', height: 36, padding: '0 12px',
          display: 'flex', alignItems: 'center', gap: 10,
          borderRadius: 6, border: 'none', cursor: 'pointer', textAlign: 'left',
          background: hover ? C.clblueSubtle : 'transparent',
          color: hover ? C.clblue500 : (hasActiveChild ? C.clblue500 : C.text),
          font: `700 14px var(--font-sans)`,
          transition: 'background 250ms cubic-bezier(0.22, 1, 0.36, 1), color 250ms cubic-bezier(0.22, 1, 0.36, 1)',
        }}>
        <span className="material-symbols-outlined" style={{
          fontSize: 18,
          color: hover ? C.clblue500 : (hasActiveChild ? C.clblue500 : '#52627a'),
          fontVariationSettings: hasActiveChild ? "'FILL' 1, 'wght' 500" : "'FILL' 0, 'wght' 400",
        }}>{item.icon}</span>
        <span style={{ flex: 1 }}>{item.label}</span>
        <span className="material-symbols-outlined" style={{
          fontSize: 18,
          color: hover ? C.clblue500 : C.textMuted,
          transition: 'transform 250ms cubic-bezier(0.22, 1, 0.36, 1)', transform: open ? 'rotate(180deg)' : 'rotate(0deg)',
        }}>expand_more</span>
      </button>
      {open && item.children && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 2, paddingTop: 2 }}>
          {item.children.map(c => (
            <LeafItem key={c.id} item={c} active={c.id === activeLeaf} onClick={() => onLeafClick(c.id)} />
          ))}
        </div>
      )}
    </div>
  );
};

const GroupTitle = ({ children }) => (
  <div style={{
    fontSize: 12, fontWeight: 500, color: C.textMuted,
    padding: '10px 12px 6px', letterSpacing: '0.01em',
  }}>{children}</div>
);

const Sidebar = ({ activeLeaf, onLeafClick, onCollapse }) => (
  <aside style={{
    width: 240, background: C.bg, borderRight: `1px solid ${C.borderStrong}`,
    display: 'flex', flexDirection: 'column', flexShrink: 0, height: '100vh',
    fontFamily: 'var(--font-sans)',
  }}>
    {/* Logo + WMS badge */}
    <div style={{
      padding: '16px 16px 12px', display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0,
    }}>
      <img src="../../assets/colo-ai-color.svg" alt="colo AI" style={{ height: 32, flex: 1, objectFit: 'contain', objectPosition: 'left center' }}/>
      <span style={{
        padding: '0 10px', background: '#FE842F', color: '#fff',
        fontSize: 13, fontWeight: 700, borderRadius: 5, letterSpacing: '0.02em',
        lineHeight: 1, height: 26, display: 'inline-flex', alignItems: 'center',
      }}>WMS</span>
    </div>

    {/* User + bell */}
    <div style={{
      padding: '0 16px', height: 36, display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0,
    }}>
      <button style={{
        width: 110, height: 32, display: 'flex', alignItems: 'center', gap: 4,
        background: 'transparent', border: 'none', cursor: 'pointer', padding: 0,
        font: `600 14px var(--font-sans)`, color: C.text,
      }}>
        <span>Jennifer B. Scott</span>
        <span className="material-symbols-outlined" style={{ fontSize: 16, color: C.textMuted }}>expand_more</span>
      </button>
      <button style={{
        position: 'relative', width: 32, height: 32, borderRadius: 6, border: 'none',
        background: 'transparent', cursor: 'pointer',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <span className="material-symbols-outlined" style={{ fontSize: 20, color: '#52627a' }}>notifications</span>
        <span style={{
          position: 'absolute', top: 2, right: 2, minWidth: 14, height: 14, padding: '0 3px',
          borderRadius: 7, background: C.dangerRed, color: '#fff',
          fontSize: 9, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>3</span>
      </button>
    </div>

    {/* Current center selector (dark card) */}
    <div style={{ padding: '0 12px 10px', flexShrink: 0 }}>
      <button style={{
        width: '100%', padding: '8px 12px 10px',
        background: C.dark, border: 'none', borderRadius: 8, cursor: 'pointer',
        display: 'flex', flexDirection: 'column', alignItems: 'stretch', gap: 4,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 11, fontWeight: 500, color: 'rgba(255,255,255,0.6)' }}>Current center</span>
          <span className="material-symbols-outlined" style={{ fontSize: 18, color: 'rgba(255,255,255,0.7)' }}>expand_more</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="material-symbols-outlined" style={{ fontSize: 16, color: '#fff' }}>home</span>
          <span style={{ fontSize: 13, fontWeight: 600, color: '#fff' }}>{'{Center name}'}</span>
        </div>
      </button>
    </div>

    {/* Search */}
    <div style={{ padding: '0 12px 16px', flexShrink: 0 }}>
      <div style={{
        position: 'relative', display: 'flex', alignItems: 'center',
        height: 32, background: '#fff',
        border: `1px solid ${C.inputBorder}`, borderRadius: 6,
      }}>
        <span className="material-symbols-outlined" style={{
          fontSize: 16, color: C.textMuted, marginLeft: 10, marginRight: 6,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          width: 16, height: 16, lineHeight: 1,
        }}>search</span>
        <input placeholder="검색" style={{
          flex: 1, minWidth: 0, height: '100%', padding: 0,
          border: 'none', outline: 'none', background: 'transparent',
          font: '500 13px var(--font-sans)', color: C.text,
        }}/>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 2,
          marginRight: 6, pointerEvents: 'none',
        }}>
          <kbd style={kbdStyle}>⌘</kbd>
          <kbd style={kbdStyle}>K</kbd>
        </div>
      </div>
    </div>

    {/* Nav (scrollable) */}
    <nav style={{
      flex: 1, overflowY: 'auto', padding: '0 8px 8px',
    }}>
      {NAV_DATA.map((sec) => (
        <div key={sec.group}>
          <GroupTitle>{sec.group}</GroupTitle>
          {sec.items.map(it => (
            <GroupItem key={it.id} item={it} activeLeaf={activeLeaf} onLeafClick={onLeafClick}/>
          ))}
        </div>
      ))}
    </nav>

    {/* Collapse footer (bottom-right) */}
    <div style={{
      padding: 10, display: 'flex', justifyContent: 'flex-end', flexShrink: 0,
      borderTop: `1px solid ${C.border}`,
    }}>
      <button onClick={onCollapse} style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        height: 28, padding: '0 8px', borderRadius: 6,
        background: '#fff', border: `1px solid ${C.borderStrong}`, cursor: 'pointer',
        font: '500 11px var(--font-sans)', color: C.textMuted,
      }}>
        <kbd style={{ ...kbdStyle, border: 'none', background: 'transparent', padding: 0 }}>⌘ + \</kbd>
        <span className="material-symbols-outlined" style={{ fontSize: 14, color: C.textMuted }}>dock_to_right</span>
      </button>
    </div>
  </aside>
);

const kbdStyle = {
  display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
  minWidth: 18, height: 18, padding: '0 4px',
  border: `1px solid ${C.borderStrong}`, borderRadius: 3, background: '#fff',
  font: '500 10px var(--font-sans)', color: C.textMuted,
};

window.Sidebar = Sidebar;
