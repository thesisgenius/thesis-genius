import React, { useState } from "react";
import { Card, CardContent } from "@/components/card";
import { Button } from "@/components/button";
import { Input } from "@/components/input";
import { Textarea } from "@/components/textarea";
import { Plus, Edit } from "lucide-react";

const initialParts = [
  {
    id: 1,
    title: "Title Page",
    content: "Edit the title page here...",
    brief: "Contains the thesis title and author information.",
  },
  {
    id: 2,
    title: "Abstract",
    content: "Write your abstract here...",
    brief: "A brief summary of your thesis.",
  },
  {
    id: 3,
    title: "Table of Contents",
    content: "Generate or write the table of contents here...",
    brief: "Lists all sections with page numbers.",
  },
];

export default function ThesisDashboard() {
  const [parts, setParts] = useState(initialParts);
  const [selectedPart, setSelectedPart] = useState(parts[0]);
  const [newPartTitle, setNewPartTitle] = useState("");

  const handlePartClick = (part) => {
    setSelectedPart(part);
  };

  const handleAddPart = () => {
    if (newPartTitle.trim()) {
      const newPart = {
        id: parts.length + 1,
        title: newPartTitle,
        content: "Edit content here...",
        brief: "No brief available.",
      };
      setParts([...parts, newPart]);
      setNewPartTitle("");
    }
  };

  const handleContentChange = (e) => {
    setSelectedPart({ ...selectedPart, content: e.target.value });
    setParts(
      parts.map((part) =>
        part.id === selectedPart.id
          ? { ...part, content: e.target.value }
          : part
      )
    );
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1">
        {/* Left Section - Parts List */}
        <div className="w-1/3 border-r p-4 bg-gray-50">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">
            Thesis Parts
          </h2>
          <div className="space-y-2">
            {parts.map((part) => (
              <Card
                key={part.id}
                className={`cursor-pointer p-2 ${
                  selectedPart.id === part.id ? "bg-blue-100" : "bg-white"
                }`}
                onClick={() => handlePartClick(part)}
              >
                <CardContent>{part.title}</CardContent>
              </Card>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-2">
            <Input
              placeholder="New Part Title"
              value={newPartTitle}
              onChange={(e) => setNewPartTitle(e.target.value)}
            />
            <Button
              onClick={handleAddPart}
              className="flex items-center justify-center"
            >
              <Plus className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Right Section - Editor */}
        <div className="w-2/3 p-4">
          <h2 className="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">
            {selectedPart.title}
          </h2>
          <Textarea
            className="w-full h-[calc(100%-2rem)] resize-none"
            value={selectedPart.content}
            onChange={handleContentChange}
          />
        </div>
      </div>

      {/* Bottom Banner */}
      <div className="w-full bg-gradient-to-r from-blue-50 to-blue-100 p-4 border-t">
        <p className="text-sm text-gray-600 text-center">
          {selectedPart.brief}
        </p>
      </div>
    </div>
  );
}
