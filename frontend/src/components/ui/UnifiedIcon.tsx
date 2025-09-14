'use client';

import React from 'react';
import {
  CheckCircle,
  TrendingUp,
  Star,
  Award,
  BookOpen,
  Target,
  Clock,
  Trophy,
  Calendar,
  FileText,
  CheckSquare,
  MessageCircle,
  Edit3,
  BarChart3,
  Activity,
  Zap,
  Users,
  Settings,
  Bell,
  Search,
  Filter,
  Download,
  Upload,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Heart,
  Share2,
  MoreHorizontal,
  X,
  Plus,
  Minus,
  ChevronDown,
  ChevronUp,
  ChevronLeft,
  ChevronRight,
  ArrowLeft,
  ArrowRight,
  ArrowUp,
  ArrowDown,
  Home,
  User,
  Mail,
  Phone,
  MapPin,
  Globe,
  Wifi,
  Battery,
  Signal,
  Volume2,
  VolumeX,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Repeat,
  Shuffle,
  Mic,
  MicOff,
  Camera,
  Video,
  Image,
  File,
  Folder,
  Database,
  Server,
  Cloud,
  Shield,
  Key,
  CreditCard,
  DollarSign,
  ShoppingCart,
  Package,
  Truck,
  Store,
  Tag,
  Percent,
  Hash,
  AtSign,
  Hash as HashIcon,
  Hash as HashIcon2
} from 'lucide-react';

interface UnifiedIconProps {
  name: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'neutral' | 'muted';
  className?: string;
}

const iconMap: { [key: string]: React.ComponentType<any> } = {
  // Icônes de base
  checkCircle: CheckCircle,
  trendingUp: TrendingUp,
  star: Star,
  award: Award,
  bookOpen: BookOpen,
  target: Target,
  clock: Clock,
  trophy: Trophy,
  calendar: Calendar,
  fileText: FileText,
  checkSquare: CheckSquare,
  messageCircle: MessageCircle,
  edit3: Edit3,
  barChart3: BarChart3,
  activity: Activity,
  zap: Zap,
  users: Users,
  settings: Settings,
  bell: Bell,
  search: Search,
  filter: Filter,
  download: Download,
  upload: Upload,
  eye: Eye,
  eyeOff: EyeOff,
  lock: Lock,
  unlock: Unlock,
  heart: Heart,
  share2: Share2,
  moreHorizontal: MoreHorizontal,
  x: X,
  plus: Plus,
  minus: Minus,
  chevronDown: ChevronDown,
  chevronUp: ChevronUp,
  chevronLeft: ChevronLeft,
  chevronRight: ChevronRight,
  arrowLeft: ArrowLeft,
  arrowRight: ArrowRight,
  arrowUp: ArrowUp,
  arrowDown: ArrowDown,
  home: Home,
  user: User,
  mail: Mail,
  phone: Phone,
  mapPin: MapPin,
  globe: Globe,
  wifi: Wifi,
  battery: Battery,
  signal: Signal,
  volume2: Volume2,
  volumeX: VolumeX,
  play: Play,
  pause: Pause,
  skipBack: SkipBack,
  skipForward: SkipForward,
  repeat: Repeat,
  shuffle: Shuffle,
  mic: Mic,
  micOff: MicOff,
  camera: Camera,
  video: Video,
  image: Image,
  file: File,
  folder: Folder,
  database: Database,
  server: Server,
  cloud: Cloud,
  shield: Shield,
  key: Key,
  creditCard: CreditCard,
  dollarSign: DollarSign,
  shoppingCart: ShoppingCart,
  package: Package,
  truck: Truck,
  store: Store,
  tag: Tag,
  percent: Percent,
  hash: HashIcon,
  atSign: AtSign
};

const sizeMap = {
  xs: 'icon-xs',
  sm: 'icon-sm',
  md: 'icon-md',
  lg: 'icon-lg',
  xl: 'icon-xl',
  '2xl': 'icon-2xl',
  '3xl': 'icon-3xl'
};

const colorMap = {
  primary: 'icon-primary',
  secondary: 'icon-secondary',
  success: 'icon-success',
  warning: 'icon-warning',
  danger: 'icon-danger',
  info: 'icon-info',
  neutral: 'icon-neutral',
  muted: 'icon-muted'
};

export default function UnifiedIcon({ 
  name, 
  size = 'md', 
  color = 'neutral',
  className = '' 
}: UnifiedIconProps) {
  const IconComponent = iconMap[name];
  
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }

  const sizeClass = sizeMap[size];
  const colorClass = colorMap[color];
  
  return (
    <IconComponent 
      className={`icon ${sizeClass} ${colorClass} ${className}`}
    />
  );
}

// Composants d'icônes spécialisés avec fond gradient
export function IconWithBackground({ 
  name, 
  backgroundType = 'primary',
  size = 'md',
  className = '' 
}: {
  name: string;
  backgroundType?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  className?: string;
}) {
  const IconComponent = iconMap[name];
  
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }

  const sizeClass = sizeMap[size];
  const backgroundClass = `icon-${backgroundType}`;
  
  return (
    <div className={`${backgroundClass} ${className}`}>
      <IconComponent className={`icon icon-white ${sizeClass}`} />
    </div>
  );
}

// Composant d'icône de statut
export function StatusIcon({ 
  status,
  className = '' 
}: {
  status: 'online' | 'offline' | 'busy' | 'away';
  className?: string;
}) {
  return (
    <div className={`icon-status icon-status-${status} ${className}`}></div>
  );
}

// Composant d'icône de carte
export function CardIcon({ 
  name, 
  cardType = 'primary',
  size = 'lg',
  className = '' 
}: {
  name: string;
  cardType?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  className?: string;
}) {
  const IconComponent = iconMap[name];
  
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }

  const sizeClass = sizeMap[size];
  const cardClass = `icon-card icon-card-${cardType}`;
  
  return (
    <div className={`${cardClass} ${className}`}>
      <IconComponent className={`icon icon-white ${sizeClass}`} />
    </div>
  );
}

