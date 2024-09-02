import { useState } from "react";
const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg bg-light">
            <div className="container-fluid">
                <a className="navbar-brand" href="#"><img src="/natural-gas-flame.png" alt="Logo" width="40" height="40" />Energy Data TT</a>
                <div class="vr"></div>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                    </ul>
                </div>
            </div>
        </nav>
    );
};
export default Navbar;
