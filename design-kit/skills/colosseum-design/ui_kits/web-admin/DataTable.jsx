// DataTable — orders list
const DataTable = ({ rows, onRow }) => (
  <div style={{ background: '#fff', border: '1px solid #e7eaef', borderRadius: 8, overflow: 'hidden' }}>
    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
      <thead>
        <tr style={{ background: '#f6f7f9', borderBottom: '1px solid #e7eaef' }}>
          {['','주문번호','고객','SKU','수량','상태','담당 FD','주문일시','']
            .map((h, i) => (
              <th key={i} style={{
                padding: '10px 12px', textAlign: i === 4 ? 'right' : 'left',
                fontSize: 12, fontWeight: 500, color: '#52627a',
                width: i === 0 ? 36 : (i === 8 ? 44 : 'auto'),
              }}>
                {i === 0 ? <input type="checkbox"/> : h}
              </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={r.id} onClick={() => onRow(r)} style={{
            borderBottom: '1px solid #f6f7f9', cursor: 'pointer',
            background: i % 2 === 0 ? '#fff' : '#fafbfc',
            transition: 'background 250ms cubic-bezier(0.22, 1, 0.36, 1)',
          }}
            onMouseEnter={e => e.currentTarget.style.background = '#e5f3ff'}
            onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? '#fff' : '#fafbfc'}>
            <td style={{ padding: '10px 12px' }}><input type="checkbox" onClick={e => e.stopPropagation()}/></td>
            <td style={{ padding: '10px 12px', fontFamily: 'var(--font-mono)', color: '#005BF6', fontWeight: 500 }}>{r.id}</td>
            <td style={{ padding: '10px 12px', color: '#29313d', fontWeight: 500 }}>{r.customer}</td>
            <td style={{ padding: '10px 12px', fontFamily: 'var(--font-mono)', color: '#464646' }}>{r.sku}</td>
            <td style={{ padding: '10px 12px', textAlign: 'right', fontFamily: 'var(--font-mono)', color: '#29313d', fontWeight: 500 }}>{r.qty.toLocaleString()}</td>
            <td style={{ padding: '10px 12px' }}><Tag variant={r.status}/></td>
            <td style={{ padding: '10px 12px', color: '#464646' }}>{r.fd}</td>
            <td style={{ padding: '10px 12px', fontFamily: 'var(--font-mono)', color: '#767676', fontSize: 12 }}>{r.date}</td>
            <td style={{ padding: '10px 12px' }}>
              <span className="material-symbols-outlined" style={{ fontSize: 18, color: '#767676' }}>chevron_right</span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 14px', borderTop: '1px solid #e7eaef' }}>
      <div style={{ fontSize: 12, color: '#767676' }}>총 <b style={{ color: '#29313d' }}>{rows.length}</b>건</div>
      <div style={{ display: 'flex', gap: 4 }}>
        {[1,2,3,4,5].map(n => (
          <button key={n} style={{
            width: 28, height: 28, borderRadius: 4,
            border: n === 1 ? '1px solid #005BF6' : '1px solid transparent',
            background: n === 1 ? '#D6ECFF' : 'transparent',
            color: n === 1 ? '#005BF6' : '#464646', fontWeight: n === 1 ? 700 : 500,
            fontSize: 13, cursor: 'pointer',
          }}>{n}</button>
        ))}
      </div>
    </div>
  </div>
);
window.DataTable = DataTable;

// OrderDetailDrawer — side drawer
const OrderDetailDrawer = ({ order, onClose }) => {
  if (!order) return null;
  const timeline = [
    { time: '14:22', label: '주문 접수', done: true },
    { time: '14:35', label: '재고 확인', done: true },
    { time: '15:10', label: '피킹 시작', done: true },
    { time: '15:45', label: '출고 대기', done: order.status !== 'cancel' },
    { time: '—', label: '출고 완료', done: false },
    { time: '—', label: '배송 완료', done: false },
  ];
  return (
    <>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.35)', zIndex: 20 }}/>
      <aside style={{
        position: 'fixed', top: 0, right: 0, bottom: 0, width: 440,
        background: '#fff', borderLeft: '1px solid #e7eaef',
        boxShadow: '0 25px 50px -12px rgba(0,0,0,0.25)', zIndex: 21,
        display: 'flex', flexDirection: 'column',
        animation: 'slideIn 0.2s ease-out',
      }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid #e7eaef', display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 11, color: '#767676' }}>주문번호</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#29313d', fontFamily: 'var(--font-mono)' }}>{order.id}</div>
          </div>
          <Tag variant={order.status}/>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: 6 }}>
            <span className="material-symbols-outlined" style={{ fontSize: 22, color: '#52627a' }}>close</span>
          </button>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: 20, display: 'flex', flexDirection: 'column', gap: 20 }}>
          <section>
            <div className="caption-hdr" style={{ fontSize: 11, color: '#767676', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 10 }}>고객 정보</div>
            <div style={{ display: 'grid', gridTemplateColumns: '80px 1fr', gap: 8, fontSize: 13 }}>
              <div style={{ color: '#767676' }}>이름</div><div style={{ color: '#29313d', fontWeight: 500 }}>{order.customer}</div>
              <div style={{ color: '#767676' }}>연락처</div><div style={{ color: '#464646', fontFamily: 'var(--font-mono)' }}>010-****-{order.id.slice(-4)}</div>
              <div style={{ color: '#767676' }}>배송지</div><div style={{ color: '#464646' }}>서울시 강남구 테헤란로 427</div>
            </div>
          </section>
          <section>
            <div className="caption-hdr" style={{ fontSize: 11, color: '#767676', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 10 }}>상품</div>
            <div style={{ border: '1px solid #e7eaef', borderRadius: 6, padding: 12, display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ width: 44, height: 44, borderRadius: 4, background: '#f6f7f9', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <span className="material-symbols-outlined" style={{ fontSize: 22, color: '#52627a' }}>package_2</span>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 500, color: '#29313d' }}>{order.customer === '삼성전자' ? '노트북 가방' : '무선 이어폰'}</div>
                <div style={{ fontSize: 11, color: '#767676', fontFamily: 'var(--font-mono)', marginTop: 2 }}>{order.sku}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: 14, fontWeight: 700, color: '#29313d', fontFamily: 'var(--font-mono)' }}>×{order.qty}</div>
              </div>
            </div>
          </section>
          <section>
            <div className="caption-hdr" style={{ fontSize: 11, color: '#767676', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 10 }}>상태 이력</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 0, position: 'relative' }}>
              {timeline.map((t, i) => (
                <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start', paddingBottom: i === timeline.length - 1 ? 0 : 14, position: 'relative' }}>
                  <div style={{ width: 16, display: 'flex', justifyContent: 'center', position: 'relative' }}>
                    <div style={{
                      width: 10, height: 10, borderRadius: '50%', marginTop: 4,
                      background: t.done ? '#005BF6' : '#fff',
                      border: t.done ? 'none' : '2px solid #CACACA',
                      zIndex: 1,
                    }}/>
                    {i !== timeline.length - 1 && <div style={{
                      position: 'absolute', top: 14, left: '50%', transform: 'translateX(-50%)',
                      width: 2, bottom: -14, background: t.done ? '#D6ECFF' : '#e7eaef',
                    }}/>}
                  </div>
                  <div style={{ flex: 1, display: 'flex', justifyContent: 'space-between' }}>
                    <div style={{ fontSize: 13, color: t.done ? '#29313d' : '#929292', fontWeight: t.done ? 500 : 400 }}>{t.label}</div>
                    <div style={{ fontSize: 12, color: '#767676', fontFamily: 'var(--font-mono)' }}>{t.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
        <div style={{ padding: 14, borderTop: '1px solid #e7eaef', display: 'flex', gap: 8 }}>
          <Button variant="outline" size="sm">이력 내보내기</Button>
          <div style={{ flex: 1 }}/>
          <Button variant="danger" size="sm">주문 취소</Button>
          <Button variant="primary" size="sm" icon="check">출고 처리</Button>
        </div>
      </aside>
      <style>{`@keyframes slideIn{from{transform:translateX(100%)}to{transform:translateX(0)}}`}</style>
    </>
  );
};
window.OrderDetailDrawer = OrderDetailDrawer;
