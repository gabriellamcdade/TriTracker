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
        <img
          src="/tritracker-logo.png"
          alt="TriTracker logo"
          className="sidebar-logo-image"
        />

        <span className="sidebar-brand-name">
          TriTracker
        </span>
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