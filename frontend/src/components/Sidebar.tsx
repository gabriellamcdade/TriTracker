type SidebarProps = {
  activePage: string;
  onPageChange: (page: string) => void;
};

function Sidebar({ activePage, onPageChange }: SidebarProps) {
  const pages = [
    "Dashboard",
    "Activities",
    "Training",
    "Recovery",
    "Goals",
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">TT</div>
        <span>TRITRACKER</span>
      </div>

      <nav className="sidebar-nav">
        {pages.map((page) => (
          <button
            key={page}
            className={`sidebar-link ${
              activePage === page ? "active" : ""
            }`}
            onClick={() => onPageChange(page)}
          >
            {page}
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;