// Header.jsx
import { Link, useNavigate } from "react-router-dom";
import Logo from "/owl.png";
import { Button } from "./ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";

import { useAuth } from "../context/authContext";
import { useThesis } from "../context/thesisContext";

export default function NewHeader() {
  const { user, signOut, refreshUser } = useAuth();
  const navigate = useNavigate();
  const { activeThesisId } = useThesis(); // <--- retrieve the ID from context

  // Logout
  const handleLogout = () => {
    signOut();
    navigate("/");
  };

  // Refresh user
  const handleRefresh = async () => {
    await refreshUser();
  };

  return (
    <header className="bg-gray-800 py-3 px-4 lg:!px-8">
      <nav className="flex justify-between items-center">
        <Link to="/" className="inline-flex gap-2 items-center">
          <img className="h-12 w-auto" src={Logo} alt="logo" />
          <div>
            <h1 className="font-bold text-2xl text-sky-300">ThesisGenius</h1>
            <p className="italic text-white">write smart, write less</p>
          </div>
        </Link>

        <Sheet>
          <SheetTrigger className="lg:hidden">
            <Menu className="text-white" />
          </SheetTrigger>
          <SheetContent className="flex flex-col pt-16">
            <Button variant="link">
              <Link to="/about">About</Link>
            </Button>
            {/*
              The link below includes the :thesisId -> /app/123/title
              or if we have none, fallback to manage-theses
            */}
            <Button variant="link">
              <Link
                to={
                  activeThesisId
                    ? `/app/${activeThesisId}/title`
                    : "/app/manage-theses"
                }
              >
                Dashboard
              </Link>
            </Button>
            <Button variant="link">
              <Link to="https://resources.nu.edu/Chatpage">Forum</Link>
            </Button>
            {user ? (
              <>
                <Button variant="link" onClick={handleRefresh}>
                  Refresh Profile
                </Button>
                <Button variant="link" onClick={handleLogout}>
                  Log out
                </Button>
              </>
            ) : (
              <>
                <Button variant="link">
                  <Link to="/signin">Sign in</Link>
                </Button>
                <Button variant="link">
                  <Link to="/signup">Register</Link>
                </Button>
              </>
            )}
          </SheetContent>
        </Sheet>

        {/* Desktop links */}
        <div className="gap-4 hidden lg:flex">
          <Button variant="link">
            <Link className="text-white" to="/about">
              About
            </Link>
          </Button>
          <Button variant="link">
            <Link
              className="text-white"
              to={
                activeThesisId
                  ? `/app/${activeThesisId}/title`
                  : "/app/manage-theses"
              }
            >
              Dashboard
            </Link>
          </Button>
          <Button variant="link">
            <Link className="text-white" to="https://resources.nu.edu/Chatpage">
              Forum
            </Link>
          </Button>
        </div>

        {/* Desktop user buttons */}
        {user ? (
          <div className="hidden lg:flex gap-4">
            <Button onClick={handleRefresh} variant="outline">
              Refresh Profile
            </Button>

            <Button onClick={handleLogout} variant="destructive">
              Log out
            </Button>
          </div>
        ) : (
          <div className="hidden lg:flex gap-4">
            <Button asChild>
              <Link to="signin">Sign In</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link to="signup">Register</Link>
            </Button>
          </div>
        )}
      </nav>
    </header>
  );
}
