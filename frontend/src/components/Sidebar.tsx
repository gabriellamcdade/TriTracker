function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">TT</div>
        <span>TRITRACKER</span>
      </div>

      <nav className="sidebar-nav">
        <button className="sidebar-link active">Dashboard</button>
        <button className="sidebar-link">Activities</button>
        <button className="sidebar-link">Training</button>
        <button className="sidebar-link">Recovery</button>
        <button className="sidebar-link">Goals</button>
      </nav>
    </aside>
  );
}

export default Sidebar;