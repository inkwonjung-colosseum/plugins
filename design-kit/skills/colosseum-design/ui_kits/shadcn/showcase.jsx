/* global React, ReactDOM, Button, Input, Textarea, Select, Field,
          Checkbox, Radio, Switch, Badge, Card, Tabs, Alert, Progress,
          Avatar, Skeleton, Tooltip, Dropdown, Dialog, Toast, Table,
          Breadcrumb, Pagination, Icon */
const { useState } = React;

function Section({ id, title, subtitle, children }) {
  return (
    <section id={id}>
      <h2>{title}</h2>
      {subtitle && <p className="section-sub">{subtitle}</p>}
      {children}
    </section>
  );
}
function Example({ label, children, col }) {
  return (
    <div className="example">
      {label && <div className="example-label">{label}</div>}
      <div className={'example-body ' + (col ? 'col' : '')}>{children}</div>
    </div>
  );
}

function App() {
  const [tab, setTab] = useState('overview');
  const [utab, setUtab] = useState('orders');
  const [sel, setSel] = useState('wh-01');
  const [sw, setSw] = useState(true);
  const [check, setCheck] = useState(true);
  const [rad, setRad] = useState('opt1');
  const [dlg, setDlg] = useState(false);
  const [toast, setToast] = useState(false);
  const [page, setPage] = useState(3);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Colosseum × shadcn</h1>
        <p>shadcn/ui 패턴 기반 · Colosseum Design System 2.0 토큰 적용</p>
        <div className="tagrow">
          <span className="tag">--clblue-500</span>
          <span className="tag">Pretendard</span>
          <span className="tag">radius-base 6px</span>
          <span className="tag">26 components</span>
        </div>
      </div>

      {/* ---------- Button ---------- */}
      <Section id="button" title="Button" subtitle="6 variants × 5 sizes · icon support · loading/disabled">
        <Example label="Variants" col>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="link">Link</Button>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
            <Button size="xs">xs</Button>
            <Button size="sm">sm</Button>
            <Button size="md">md</Button>
            <Button size="lg">lg</Button>
            <Button size="xl">xl</Button>
          </div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <Button icon="add">입고 등록</Button>
            <Button variant="outline" icon="download">Export</Button>
            <Button variant="ghost" icon="more_horiz" iconOnly aria-label="더보기" />
            <Button variant="primary" disabled>Disabled</Button>
          </div>
        </Example>
      </Section>

      {/* ---------- Input ---------- */}
      <Section id="input" title="Input · Textarea · Label" subtitle="label / helper / error states">
        <Example>
          <div className="grid-3" style={{ width: '100%' }}>
            <Field label="이름" required helper="실명을 입력해주세요">
              <Input placeholder="홍길동" />
            </Field>
            <Field label="이메일" error="유효하지 않은 이메일입니다">
              <Input value="test@" error onChange={() => {}} />
            </Field>
            <Field label="비활성">
              <Input disabled placeholder="수정 불가" />
            </Field>
          </div>
          <Field label="메모" helper="최대 500자">
            <Textarea placeholder="입고 시 특이사항을 입력하세요..." />
          </Field>
        </Example>
      </Section>

      {/* ---------- Select ---------- */}
      <Section id="select" title="Select" subtitle="custom dropdown with keyboard support">
        <Example>
          <div style={{ width: 280 }}>
            <Field label="출고 창고">
              <Select value={sel} onChange={setSel} options={[
                { value: 'wh-01', label: '서울 1센터 (SEL-01)' },
                { value: 'wh-02', label: '인천 허브 (ICN-HUB)' },
                { value: 'wh-03', label: '부산 2센터 (BSN-02)' },
                { value: 'wh-04', label: '대전 분기 (DJN-BR)' },
              ]} />
            </Field>
          </div>
        </Example>
      </Section>

      {/* ---------- Checkbox / Radio / Switch ---------- */}
      <Section id="form-controls" title="Checkbox · Radio · Switch">
        <Example>
          <div style={{ display: 'flex', gap: 32 }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <Checkbox label="전체 선택" checked={check} onChange={e => setCheck(e.target.checked)} />
              <Checkbox label="입고 알림" defaultChecked />
              <Checkbox label="비활성" disabled />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <Radio label="일반 출고" name="r" value="opt1" checked={rad === 'opt1'} onChange={e => setRad(e.target.value)} />
              <Radio label="긴급 출고" name="r" value="opt2" checked={rad === 'opt2'} onChange={e => setRad(e.target.value)} />
              <Radio label="예약 출고" name="r" value="opt3" checked={rad === 'opt3'} onChange={e => setRad(e.target.value)} />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <Switch checked={sw} onChange={setSw} label="자동 배차" />
              <Switch checked={false} onChange={() => {}} label="SMS 알림" />
            </div>
          </div>
        </Example>
      </Section>

      {/* ---------- Badge ---------- */}
      <Section id="badge" title="Badge · Tag" subtitle="status indicators · 7 semantic variants">
        <Example>
          <Badge variant="primary">입고중</Badge>
          <Badge variant="success" dot>정상</Badge>
          <Badge variant="warning">지연</Badge>
          <Badge variant="danger" dot>오류</Badge>
          <Badge variant="info">대기</Badge>
          <Badge variant="neutral">초안</Badge>
          <Badge variant="outline">외부</Badge>
        </Example>
      </Section>

      {/* ---------- Card ---------- */}
      <Section id="card" title="Card">
        <Example>
          <div className="grid-2" style={{ width: '100%' }}>
            <Card title="금일 입고" description="2026-04-21 기준">
              <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--natural-700)' }}>1,284 <span style={{ fontSize: 14, color: 'var(--gray-500)', fontWeight: 500 }}>건</span></div>
              <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
                <Badge variant="success" dot>+12.4%</Badge>
                <span style={{ fontSize: 12, color: 'var(--gray-500)' }}>전일 대비</span>
              </div>
            </Card>
            <Card title="출고 진행" description="실시간" footer={<><Button variant="outline" size="sm">상세</Button><Button size="sm">새 출고</Button></>}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}><span>피킹</span><span style={{ fontWeight: 600 }}>72%</span></div>
                <Progress value={72} />
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}><span>패킹</span><span style={{ fontWeight: 600 }}>45%</span></div>
                <Progress value={45} />
              </div>
            </Card>
          </div>
        </Example>
      </Section>

      {/* ---------- Tabs ---------- */}
      <Section id="tabs" title="Tabs" subtitle="pill (segmented) and underline variants">
        <Example col>
          <Tabs value={tab} onChange={setTab} tabs={[
            { value: 'overview', label: '개요' },
            { value: 'inbound', label: '입고' },
            { value: 'outbound', label: '출고' },
            { value: 'inventory', label: '재고' },
          ]} />
          <Tabs variant="underline" value={utab} onChange={setUtab} tabs={[
            { value: 'orders', label: '주문 목록' },
            { value: 'waves', label: '웨이브' },
            { value: 'picking', label: '피킹' },
            { value: 'shipping', label: '출고 확정' },
          ]} />
        </Example>
      </Section>

      {/* ---------- Alert ---------- */}
      <Section id="alert" title="Alert" subtitle="inline status messages">
        <Example col>
          <Alert variant="info" title="새 기능 안내">재고 실사 자동화 기능이 추가되었습니다. 관리자 설정에서 활성화하세요.</Alert>
          <Alert variant="success" title="저장 완료">주문 3건이 정상적으로 저장되었습니다.</Alert>
          <Alert variant="warning" title="임계치 경고">재고 5건이 안전 재고 이하로 떨어졌습니다.</Alert>
          <Alert variant="danger" title="연동 실패">ERP 동기화 중 오류가 발생했습니다. 관리자에게 문의하세요.</Alert>
        </Example>
      </Section>

      {/* ---------- Table ---------- */}
      <Section id="table" title="Table" subtitle="hoverable rows with semantic header background">
        <Example col>
          <Table
            columns={[
              { key: 'id', label: '주문번호', width: 140 },
              { key: 'customer', label: '고객명' },
              { key: 'status', label: '상태', render: r => <Badge variant={r.statusVariant}>{r.status}</Badge> },
              { key: 'qty', label: '수량', align: 'right', render: r => r.qty.toLocaleString() },
              { key: 'date', label: '등록일', width: 120 },
              { key: 'actions', label: '', width: 40, render: () => (
                <Dropdown trigger={<button className="btn btn-ghost btn-xs btn-icon"><Icon name="more_vert" size={16} /></button>}
                  items={[{ icon: 'visibility', label: '상세' }, { icon: 'edit', label: '수정' }, { separator: true }, { icon: 'delete', label: '삭제', danger: true }]} />
              )},
            ]}
            rows={[
              { id: 'SO-24042101', customer: '콜로세움 마켓', status: '출고 완료', statusVariant: 'success', qty: 120, date: '04-21' },
              { id: 'SO-24042102', customer: '스마일박스',   status: '피킹중',    statusVariant: 'primary', qty: 56,  date: '04-21' },
              { id: 'SO-24042103', customer: '하나로유통',   status: '대기',       statusVariant: 'info',    qty: 380, date: '04-21' },
              { id: 'SO-24042104', customer: 'ABC 코리아',   status: '지연',       statusVariant: 'warning', qty: 12,  date: '04-20' },
              { id: 'SO-24042105', customer: 'GS 로지스',    status: '취소',       statusVariant: 'danger',  qty: 0,   date: '04-20' },
            ]}
          />
          <Pagination page={page} total={8} onChange={setPage} />
        </Example>
      </Section>

      {/* ---------- Dialog / Toast / Tooltip / Dropdown ---------- */}
      <Section id="overlays" title="Dialog · Toast · Tooltip · Dropdown" subtitle="overlay primitives">
        <Example>
          <Button onClick={() => setDlg(true)}>Open Dialog</Button>
          <Button variant="outline" onClick={() => { setToast(true); setTimeout(() => setToast(false), 3000); }}>Show Toast</Button>
          <Tooltip content="입고 완료 건수"><Button variant="outline" icon="help">Hover me</Button></Tooltip>
          <Dropdown trigger={<Button variant="outline" icon="expand_more">Actions</Button>}
            items={[
              { icon: 'edit', label: '수정' },
              { icon: 'content_copy', label: '복제' },
              { icon: 'archive', label: '보관' },
              { separator: true },
              { icon: 'delete', label: '삭제', danger: true },
            ]} />
        </Example>
        <Dialog open={dlg} onClose={() => setDlg(false)} title="주문을 취소하시겠습니까?" description="이 작업은 되돌릴 수 없습니다. 취소된 주문은 이력에서만 조회됩니다."
          footer={<><Button variant="outline" onClick={() => setDlg(false)}>닫기</Button><Button variant="destructive" onClick={() => setDlg(false)}>주문 취소</Button></>} />
        {toast && (
          <div style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 100 }}>
            <Toast variant="success" title="저장되었습니다" description="3건의 주문이 업데이트되었습니다." onClose={() => setToast(false)} />
          </div>
        )}
      </Section>

      {/* ---------- Avatar · Progress · Skeleton · Breadcrumb ---------- */}
      <Section id="misc" title="Avatar · Progress · Skeleton · Breadcrumb">
        <Example col>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <Avatar initials="김" size="sm" />
            <Avatar initials="박" />
            <Avatar initials="JS" size="lg" />
            <div style={{ display: 'flex' }}>
              {['김','이','박','최'].map((n, i) => (
                <div key={i} style={{ marginLeft: i === 0 ? 0 : -8, border: '2px solid #fff', borderRadius: '50%' }}>
                  <Avatar initials={n} size="sm" />
                </div>
              ))}
            </div>
          </div>
          <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 10 }}>
            <Progress value={25} /><Progress value={60} /><Progress value={92} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, width: 400 }}>
            <Skeleton height={16} width="60%" />
            <Skeleton height={12} />
            <Skeleton height={12} width="80%" />
          </div>
          <Breadcrumb items={[
            { label: '홈', href: '#' },
            { label: '주문 관리', href: '#' },
            { label: '출고 목록', href: '#' },
            { label: 'SO-24042101' },
          ]} />
        </Example>
      </Section>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
