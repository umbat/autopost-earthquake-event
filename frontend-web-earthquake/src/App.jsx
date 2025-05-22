import React, { useState, useEffect } from 'react';
import { Home, FileText, Settings, Clock, RotateCcw, User, Menu, X, ChevronDown } from 'lucide-react';

export default function EarthquakeDashboard() {
  const [selectedParameter, setSelectedParameter] = useState('PGR II');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedDuty, setSelectedDuty] = useState('On Duty 1');
  const [dutyDropdownOpen, setDutyDropdownOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  const dutyOptions = ['On Duty 1', 'On Duty 2', 'On Duty 3'];

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Format time for display
  const formatTime = (date, timezone) => {
    if (timezone === 'UTC') {
      return {
        time: date.toUTCString().slice(17, 25),
        date: date.toUTCString().slice(0, 16)
      };
    } else {
      // WIB is UTC+7
      const wibTime = new Date(date.getTime() + (7 * 60 * 60 * 1000));
      return {
        time: wibTime.toUTCString().slice(17, 25),
        date: wibTime.toUTCString().slice(0, 16)
      };
    }
  };

  const utcTime = formatTime(currentTime, 'UTC');
  const wibTime = formatTime(currentTime, 'WIB');

  return (
    <div className="flex h-screen bg-gray-50 relative">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-white shadow-sm transition-all duration-300 overflow-hidden fixed h-full z-20`}>
        {/* Logo */}
        <div className="p-4 border-b">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <span className="text-white text-xs font-bold">AP</span>
            </div>
            <div>
              <h1 className="font-semibold text-gray-800">Autopost Platform</h1>
              <p className="text-xs text-gray-500">Balai Besar MKG Wilayah II</p>
            </div>
          </div>
        </div>

        {/* User Info */}
        <div className="p-4 border-b">
          <div className="flex items-center gap-3">
            <User className="w-8 h-8 text-gray-400" />
            <div>
              <p className="font-medium text-gray-700">PUSAT GEMPA</p>
              <p className="text-sm text-gray-500">REGIONAL II</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4">
          <div className="space-y-2">
            <div className="flex items-center gap-3 p-3 bg-gray-100 rounded-lg">
              <Home className="w-5 h-5 text-gray-600" />
              <span className="font-medium text-gray-800">Dashboard</span>
            </div>
            <div className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <FileText className="w-5 h-5 text-gray-400" />
              <span className="text-gray-600">Log</span>
            </div>
            <div className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <Settings className="w-5 h-5 text-gray-400" />
              <span className="text-gray-600">Settings</span>
            </div>
          </div>
        </nav>
      </div>

      {/* Sidebar Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-10 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-0'}`}>
        {/* Header */}
        <header className="bg-white shadow-sm p-3 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-4">
            {/* Hamburger Menu */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100"
            >
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center gap-8">
            <button className="text-blue-600 font-medium border-b-2 border-blue-600 pb-1">Weighting</button>
            <button className="text-gray-500 hover:text-gray-700">Dissemination</button>
            <button className="text-gray-500 hover:text-gray-700">Narration</button>
            <button className="text-gray-400">Admin</button>
            <button className="text-gray-400">•••</button>
          </div>

          {/* Live Time Display */}
          <div className="flex items-center gap-2">
            <div className="text-xl font-bold text-gray-800">UTC :</div>
            <div className="flex items-center gap-2 bg-green-200 rounded px-4 py-2 ">
              <div className="text-left">
                <div className="text-2xl font-bold text-gray-800">{utcTime.time}</div>
                <div className="text-sm text-gray-500">{utcTime.date}</div>
              </div>
            </div>
            <div className="text-xl font-bold text-gray-800">WIB :</div>
            <div className="flex items-center gap-2 bg-green-200 rounded px-4 py-2 ">
              <div className="text-left">
                <div className="text-2xl font-bold text-gray-800">{wibTime.time}</div>
                <div className="text-sm text-gray-500">{wibTime.date}</div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="flex-1 p-6 space-y-6 overflow-auto">
          {/* Top Row */}
          <div className="grid grid-cols-3 gap-6">
            {/* Geophysics On Duty - Now with Dropdown */}
            <div className="bg-white rounded-lg shadow-sm p-4">
              <h3 className="font-medium text-gray-700 mb-3">Geophysics On Duty</h3>
              <div className="relative">
                <button
                  onClick={() => setDutyDropdownOpen(!dutyDropdownOpen)}
                  className="flex items-center justify-between w-full p-2 border rounded-lg hover:bg-gray-50"
                >
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="text-sm text-gray-700">{selectedDuty}</span>
                  </div>
                  <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${dutyDropdownOpen ? 'rotate-180' : ''}`} />
                </button>
                
                {dutyDropdownOpen && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg z-20">
                    {dutyOptions.map((option) => (
                      <button
                        key={option}
                        onClick={() => {
                          setSelectedDuty(option);
                          setDutyDropdownOpen(false);
                        }}
                        className="w-full text-left p-2 hover:bg-gray-50 flex items-center gap-2 first:rounded-t-lg last:rounded-b-lg"
                      >
                        <User className="w-4 h-4 text-gray-500" />
                        <span className="text-sm text-gray-700">{option}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Gempa Terakhir */}
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-500">Gempa Terakhir</span>
                <span className="bg-green-500 text-white px-2 py-1 rounded text-xs">2.3 SR</span>
              </div>
              <h3 className="font-medium text-gray-800">Pesisir Barat, Lampung</h3>
              <p className="text-sm text-gray-500">19.14.55 (33 minutes ago)</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white rounded-lg shadow-sm p-4">
                <div className="text-sm text-gray-500 mb-1">Total Gempa M{'<'}5.0</div>
                <div className="text-sm text-gray-500 mb-2">Hari Ini</div>
                <div className="flex items-center gap-2">
                  <span className="text-3xl font-bold text-gray-800">8</span>
                  <span className="text-green-600 text-sm">+11%</span>
                </div>
              </div>
              <div className="bg-white rounded-lg shadow-sm p-4">
                <div className="text-sm text-gray-500 mb-1">Total Gempa M{'<'}5.0</div>
                <div className="text-sm text-gray-500 mb-2">Bulan Ini</div>
                <div className="flex items-center gap-2">
                  <span className="text-3xl font-bold text-gray-800">46</span>
                  <span className="text-green-600 text-sm">+5.2%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Middle Row - Status Cards */}
          <div className="grid grid-cols-2 gap-6">
            {/* ESDX */}
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-800">ESDX</h3>
                <RotateCcw className="w-4 h-4 text-gray-400" />
              </div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Updated 5 seconds ago</span>
              </div>
              <div className="grid grid-cols-4 gap-2 text-sm">
                <div className="font-medium text-gray-700 px-2">Lokasi</div>
                <div className="font-medium text-gray-700 col-span-3 px-2">Isi Informasi</div>
              </div>
              <div className="space-y-2 mt-2">
                <div className="bg-green-500 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">Balai 2 Ciputat</div>
                  <div className="col-span-3 p-2">Mag: 3.9 14-Mei-25 04:55 WIB,Lok: 5.57 LS - 105.60 BT</div>
                </div>
                <div className="bg-yellow-400 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">Balai 2 Ciputat</div>
                  <div className="col-span-3 p-2">Mag: 2.1 14-Mei-25 01:59:23 WIB,Lok: 4.16 LS - 104.13 BT</div>
                </div>
                <div className="bg-gray-200 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">Balai 2 Ciputat</div>
                  <div className="col-span-3 p-2">Mag: 2.1 14-Mei-25 00:49:29 WIB,Lok: 2.43 LS - 102.40 BT</div>
                </div>
                <div className="bg-gray-200 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">Balai 2 Ciputat</div>
                  <div className="col-span-3 p-2">Mag: 2.2 14-Mei-25 00:09:21 WIB,Lok: 2.32 LS - 102.29 BT</div>
                </div>
                <div className="bg-gray-200 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">Balai 2 Ciputat</div>
                  <div className="col-span-3 p-2">Mag: 2.6 14-Mei-25 00:03:41 WIB,Lok: 2.63 LS - 102.42 BT</div>
                </div>
              </div>
            </div>

            {/* ESDX STASIUN */}
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-800">ESDX STASIUN</h3>
                <RotateCcw className="w-4 h-4 text-gray-400" />
              </div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Updated 5 seconds ago</span>
              </div>
              <div className="grid grid-cols-4 gap-2 text-sm">
                <div className="font-medium text-gray-700 px-2">Lokasi</div>
                <div className="font-medium text-gray-700 col-span-3 px-2">Isi Informasi</div>
              </div>
              <div className="space-y-2 mt-2">
                <div className="bg-green-500 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">BMKG Bengkulu</div>
                  <div className="col-span-3 p-2">Mag: 3.9 14-Mei-25 04:55 WIB,Lok: 5.57 LS - 105.60 BT</div>
                </div>
                <div className="bg-yellow-400 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">BMKG Kotabumi</div>
                  <div className="col-span-3 p-2">Mag: 2.1 14-Mei-25 01:59:23 WIB,Lok: 4.16 LS - 104.13 BT</div>
                </div>
                <div className="bg-green-500 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">BMKG Kepahiang</div>
                  <div className="col-span-3 p-2">Mag: 3.9 14-Mei-25 04:55 WIB,Lok: 5.57 LS - 105.60 BT</div>
                </div>
                <div className="bg-green-500 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">BMKG Bengkulu</div>
                  <div className="col-span-3 p-2">Mag: 3.9 14-Mei-25 04:55 WIB,Lok: 5.57 LS - 105.60 BT</div>
                </div>
                <div className="bg-red-500 text-black rounded text-sm font-semibold grid grid-cols-4 gap-2">
                  <div className="p-2">BMKG Sukabumi</div>
                  <div className="col-span-3 p-2">Mag: 2.6 14-Mei-25 00:03:41 WIB,Lok: 2.63 LS - 102.42 BT</div>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Row */}
          <div className="grid grid-cols-3 gap-6">
            {/* Weighting Table */}
            <div className="col-span-2 bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-800 mb-4">WEIGHTING</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b grid grid-cols-8 gap-2 bg-gray-100">
                      <th className="text-left px-2 py-2">SITE</th>
                      <th className="text-center py-2">+/- H</th>
                      <th className="text-center py-2">+/- Lat</th>
                      <th className="text-center py-2">+/- Lon</th>
                      <th className="text-center py-2">RMS</th>
                      <th className="text-center py-2">Phase</th>
                      <th className="text-center py-2">Az</th>
                      <th className="text-center py-2 bg-green-500 text-black font-semibold">Rank</th>
                    </tr>
                  </thead>
                  <tbody className="text-center">
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">PGR II</td>
                      <td>7</td><td>7</td><td>7</td><td>7</td><td>7</td><td>7</td><td className="bg-green-500 text-black font-semibold">7</td>
                    </tr>
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">KLI</td>
                      <td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td>5</td><td className="bg-green-500 text-black font-semibold">5</td>
                    </tr>
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">LEM</td>
                      <td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td className="bg-green-500 text-black font-semibold">1</td>
                    </tr>
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">TNG</td>
                      <td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td className="bg-green-500 text-black font-semibold">2</td>
                    </tr>
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">KSI</td>
                      <td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td className="bg-green-500 text-black font-semibold">9</td>
                    </tr>
                    <tr className="border-b grid grid-cols-8 gap-2">
                      <td className="px-2 py-2 text-left">SKJI</td>
                      <td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td className="bg-green-500 text-black font-semibold">4</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div className="mt-6">
                <div className="text-center font-medium text-gray-700 mb-3">PARAMETER TERPILIH : PGR II</div>
                <div className="text-center mb-3">
                  <div className="text-center inline-block font-medium text-xl text-gray-700 mb-3 px-6 py-2 rounded bg-green-500">PGR II</div>
                </div>
                <div className="flex justify-center gap-4">
                  {['PGR II', 'KLI', 'LEM', 'TNG', 'KSI', 'SKJI'].map((param) => (
                    <label key={param} className="flex items-center">
                      <input
                        type="radio"
                        name="parameter"
                        value={param}
                        checked={selectedParameter === param}
                        onChange={(e) => setSelectedParameter(e.target.value)}
                        className="mr-2"
                      />
                      <span className="text-sm">{param}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="mt-4 text-center">
                <button className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-700">
                  Generate Image
                </button>
              </div>
            </div>

            {/* Generated Image */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-800 mb-4">GENERATED IMAGE</h3>
              <div className="relative px-8">
                <img 
                  src="/assets/earthquake_map.png" 
                  alt="Generated earthquake map"
                  className="w-full"
                />
            
              </div>
              <div className="mt-4 text-center">
                <button className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600">
                  Save Image
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}