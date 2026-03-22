import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

 
  useEffect(() => {
    if (!loading) {
      inputRef.current?.focus();
    }
  }, [loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/query", {
        query: input,
      });

      const botMessage = { role: "bot", text: res.data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error connecting to server." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-6 shadow-2xl border-b border-purple-500/20">
        <h1 className="text-3xl font-bold flex items-center gap-3 bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
          <span className="text-4xl">🚀</span>
          RAG Assistant
        </h1>
        <p className="text-purple-200 text-sm mt-1">Ask anything, get insights powered by RAG</p>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
        {messages.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center opacity-50">
            <div className="text-6xl mb-4">💬</div>
            <p className="text-xl font-semibold mb-2">Start a conversation</p>
            <p className="text-gray-400">Ask me anything about your documents</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 mb-4 animate-fadeIn ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.role === "bot" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-sm font-bold">🤖</div>
            )}
            <div
              className={`max-w-2xl px-4 py-3 rounded-2xl break-words shadow-lg transition-all hover:shadow-xl ${
                msg.role === "user"
                  ? "bg-gradient-to-r from-blue-600 to-blue-500 rounded-bl-none"
                  : "bg-slate-700/80 backdrop-blur-sm rounded-tl-none border border-slate-600/50"
              }`}
            >
              {msg.role === "bot" ? (
                <ReactMarkdown
                  children={msg.text}
                  components={{
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <SyntaxHighlighter
                          style={oneDark}
                          language={match[1]}
                          PreTag="div"
                          className="rounded-lg my-2"
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code className="bg-slate-800 px-2 py-1 rounded text-yellow-300 font-mono text-sm" {...props}>
                          {children}
                        </code>
                      );
                    },
                    p({ children }) {
                      return <p className="mb-2 last:mb-0">{children}</p>;
                    },
                    ul({ children }) {
                      return <ul className="list-disc list-inside mb-2 ml-2">{children}</ul>;
                    },
                    ol({ children }) {
                      return <ol className="list-decimal list-inside mb-2 ml-2">{children}</ol>;
                    },
                    h1({ children }) {
                      return <h1 className="text-lg font-bold mb-2 mt-2">{children}</h1>;
                    },
                    h2({ children }) {
                      return <h2 className="text-base font-bold mb-2 mt-2">{children}</h2>;
                    },
                    a({ href, children }) {
                      return (
                        <a
                          href={href}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-300 underline hover:text-blue-200 transition-colors"
                        >
                          {children}
                        </a>
                      );
                    },
                  }}
                />
              ) : (
                <span className="text-white">{msg.text}</span>
              )}
            </div>
            {msg.role === "user" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center text-sm font-bold">👤</div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 mb-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-sm font-bold">🤖</div>
            <div className="bg-slate-700/80 backdrop-blur-sm px-4 py-3 rounded-2xl rounded-tl-none border border-slate-600/50 shadow-lg">
              <div className="flex gap-1 items-center">
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></span>
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></span>
              </div>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Box */} 
      <div className="p-6 border-t border-slate-700/50 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 shadow-2xl">
        <div className="flex gap-3">
          <input
            ref={inputRef}
            className="flex-1 px-4 py-3 rounded-xl bg-slate-700/50 backdrop-blur-sm border border-slate-600 focus:border-purple-500 outline-none focus:shadow-lg focus:shadow-purple-500/20 transition-all placeholder-slate-400 text-white"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !loading && sendMessage()}
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl hover:from-purple-500 hover:to-blue-500 transition-all shadow-lg hover:shadow-purple-500/50 font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {loading ? "⏳" : "📤"}
            {!loading && "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}