import React, { useEffect, useState, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import userAPI from "@/services/userEndpoint";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export default function ProfilePage() {
  const { refreshUser } = useAuth();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  // Cache the user profile to avoid redundant fetch calls
  const profileCache = useRef(null);

  // Fetch Profile
  const fetchProfile = useCallback(async () => {
    if (profileCache.current) {
      // If we already have cached data, use it
      setProfile(profileCache.current);
      setLoading(false);
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/signin");
        return;
      }

      // Fetch user profile
      const [userProfile] = await Promise.all([
        userAPI.getUserProfile(),
      ]);

      const userData = userProfile.user ?? {};
      profileCache.current = userData; // Cache the user data
      setProfile(userData);
      refreshUser();
    } catch (error) {
      console.error("Error loading profile:", error);
      setError("Failed to load profile. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [navigate, refreshUser]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  // Handle changes to text inputs
  const handleChange = (e) => {
    setProfile((prevProfile) => ({
      ...prevProfile,
      [e.target.id]: e.target.value,
    }));
  };

  // Save text fields
  const handleSave = async () => {
    if (!profile) return;
    if (!profile.first_name || !profile.last_name || !profile.email) {
      alert("First name, last name, and email are required.");
      return;
    }

    try {
      const updatedProfile = {
        first_name: profile.first_name.trim(),
        last_name: profile.last_name.trim(),
        email: profile.email.trim(),
        institution: profile.institution?.trim() || "",
      };

      console.log("Updating profile with:", updatedProfile);
      await userAPI.updateUserProfile(updatedProfile);

      // Update cache
      profileCache.current = updatedProfile;

      await refreshUser();
      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error.response?.data || error);
      alert(`Failed to update profile: ${error.response?.data?.message || "Unexpected error"}`);
    }
  };

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) setSelectedFile(file);
  };

  // Upload Picture
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please choose a file first.");
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("profile_picture", selectedFile);

      console.log("Uploading profile picture...");
      const response = await userAPI.uploadProfilePicture(formData);

      if (response.success) {
        alert("Profile picture updated successfully!");
        // Refresh to get the new image path
        await fetchProfile();
      } else {
        throw new Error(response.message || "Failed to upload image");
      }
    } catch (error) {
      console.error("Error uploading profile picture:", error);
      alert("Failed to upload profile picture.");
    } finally {
      setUploading(false);
      setSelectedFile(null); // Reset file selection
    }
  };

  if (error) {
    return (
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8">Profile</h1>
          <div className="text-red-600 text-lg mb-4">{error}</div>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
    );
  }

  if (loading || !profile) {
    return (
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8">Loading profile...</h1>
        </div>
    );
  }

  return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Your Profile</h1>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Profile Picture Card */}
          <Card className="shadow-md">
            <CardHeader>
              <CardTitle className="text-xl font-bold">Profile Picture</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center space-y-4">
              <Avatar className="w-32 h-32">
                <AvatarImage
                    src={profile.profile_picture || "/placeholder-avatar.jpg"}
                    alt="Profile Picture"
                />
                <AvatarFallback>
                  {profile.first_name && profile.last_name ? profile.first_name.charAt(0) + profile.last_name.charAt(0) : "PP"}
                </AvatarFallback>
              </Avatar>

              <div className="flex flex-col items-center space-y-2">
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-100 file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0 file:text-sm file:font-semibold
                  file:bg-blue-600 file:text-white hover:file:bg-blue-700
                  cursor-pointer"
                />
                <Button onClick={handleUpload} disabled={uploading} className="w-full md:w-auto">
                  {uploading ? "Uploading..." : "Upload Picture"}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Personal Information Card */}
          <Card className="shadow-md">
            <CardHeader>
              <CardTitle className="text-xl font-bold">Personal Information</CardTitle>
              <CardDescription>Update your personal details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium mb-1">
                  First Name
                </label>
                <Input
                    id="first_name"
                    value={profile.first_name ?? ""}
                    onChange={handleChange}
                />
              </div>

              <div>
                <label htmlFor="last_name" className="block text-sm font-medium mb-1">
                  Last Name
                </label>
                <Input
                    id="last_name"
                    value={profile.last_name ?? ""}
                    onChange={handleChange}
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium mb-1">
                  Email
                </label>
                <Input
                    id="email"
                    type="email"
                    value={profile.email ?? ""}
                    readOnly
                    className="bg-gray-800 cursor-not-allowed"
                />
                <p className="text-xs text-gray-500">
                  Validated email address for account (cannot change).
                </p>
              </div>

              <div>
                <label htmlFor="institution" className="block text-sm font-medium mb-1">
                  Institution
                </label>
                <Input
                    id="institution"
                    value={profile.institution ?? ""}
                    onChange={handleChange}
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button onClick={handleSave} className="ml-auto">
                Save Changes
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
  );
}
