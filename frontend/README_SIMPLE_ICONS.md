# Système d'icônes simples et épurées

## Vue d'ensemble

Ce système d'icônes simples utilise des formes géométriques basiques et des symboles minimalistes pour créer une interface épurée et moderne. Toutes les icônes sont dessinées avec des traits fins et des formes géométriques simples.

## Caractéristiques

### 🎨 Style minimaliste
- **Formes géométriques** : Cercle, carré, triangle, diamant, hexagone
- **Symboles simples** : Étoile, cœur, flèches, coche, croix
- **Traits fins** : `stroke-width: 2` pour toutes les icônes
- **Design épuré** : Pas de détails superflus, juste l'essentiel

### 📏 Tailles standardisées
- `xs` : 12px × 12px
- `sm` : 16px × 16px
- `md` : 20px × 20px
- `lg` : 24px × 24px
- `xl` : 32px × 32px
- `2xl` : 40px × 40px
- `3xl` : 48px × 48px

### 🌈 Palette de couleurs cohérente
- **Primary** : Bleu (#3B82F6)
- **Secondary** : Violet (#8B5CF6)
- **Success** : Vert (#10B981)
- **Warning** : Orange (#F59E0B)
- **Danger** : Rouge (#EF4444)
- **Info** : Bleu ciel (#0EA5E9)
- **Neutral** : Gris (#737373)
- **Muted** : Gris clair (#94A3B8)

## Composants disponibles

### 1. SimpleIcon
Icône simple avec style minimaliste.

```tsx
import SimpleIcon from '../components/ui/SimpleIcon';

<SimpleIcon 
  name="circle" 
  size="lg" 
  color="primary" 
/>
```

### 2. SimpleIconWithBackground
Icône simple avec fond gradient coloré.

```tsx
import { SimpleIconWithBackground } from '../components/ui/SimpleIcon';

<SimpleIconWithBackground 
  name="star" 
  backgroundType="warning" 
  size="lg" 
/>
```

### 3. SimpleStatusIcon
Petit indicateur de statut circulaire.

```tsx
import { SimpleStatusIcon } from '../components/ui/SimpleIcon';

<SimpleStatusIcon status="online" />
```

### 4. SimpleCardIcon
Icône simple dans un conteneur de carte avec ombre.

```tsx
import { SimpleCardIcon } from '../components/ui/SimpleIcon';

<SimpleCardIcon 
  name="grid" 
  cardType="info" 
  size="lg" 
/>
```

## Noms d'icônes disponibles

### Formes géométriques basiques
- `circle` - Cercle
- `square` - Carré
- `triangle` - Triangle
- `diamond` - Diamant
- `hexagon` - Hexagone

### Symboles simples
- `star` - Étoile
- `heart` - Cœur
- `plus` - Plus
- `minus` - Moins
- `check` - Coche
- `x` - Croix
- `dot` - Point
- `line` - Ligne

### Flèches de navigation
- `arrow-up` - Flèche vers le haut
- `arrow-down` - Flèche vers le bas
- `arrow-left` - Flèche vers la gauche
- `arrow-right` - Flèche vers la droite

### Icônes utilitaires
- `grid` - Grille
- `list` - Liste
- `menu` - Menu hamburger
- `search` - Loupe de recherche
- `settings` - Roue dentée
- `user` - Silhouette d'utilisateur
- `home` - Maison
- `mail` - Enveloppe
- `phone` - Téléphone
- `calendar` - Calendrier
- `clock` - Horloge
- `book` - Livre
- `file` - Document
- `folder` - Dossier

### Icônes d'action
- `download` - Téléchargement
- `upload` - Upload
- `lock` - Cadenas fermé
- `unlock` - Cadenas ouvert
- `eye` - Œil (visible)
- `eye-off` - Œil barré (caché)
- `bell` - Cloche/notification
- `trash` - Poubelle
- `edit` - Crayon d'édition
- `share` - Partager
- `more` - Plus d'options

## Utilisation dans les composants

### Exemple d'utilisation dans un widget

```tsx
import SimpleIcon, { SimpleIconWithBackground } from '../components/ui/SimpleIcon';

export default function MonWidget() {
  return (
    <div className="card-unified">
      <div className="card-unified-header">
        <div className="flex items-center gap-3">
          <SimpleIconWithBackground 
            name="star" 
            backgroundType="warning" 
            size="lg" 
          />
          <h2 className="text-xl font-bold text-primary">Mon Widget</h2>
        </div>
      </div>
      <div className="card-unified-body">
        <div className="flex items-center gap-2">
          <SimpleIcon name="check" size="sm" color="success" />
          <span>Élément avec icône</span>
        </div>
      </div>
    </div>
  );
}
```

### Exemple d'utilisation dans un bouton

```tsx
import SimpleIcon from '../components/ui/SimpleIcon';

<button className="btn-unified btn-unified-primary">
  <SimpleIcon name="plus" size="sm" color="white" />
  Ajouter
</button>
```

### Exemple d'utilisation pour les statistiques

```tsx
import SimpleIcon from '../components/ui/SimpleIcon';

<div className="card-stat card-stat-primary">
  <div className="card-stat-icon">
    <SimpleIcon name="check" size="lg" color="white" />
  </div>
  <div className="card-stat-value">42</div>
  <div className="card-stat-label">Quiz Complétés</div>
</div>
```

## Classes CSS disponibles

### Classes de base
- `.icon` - Style de base pour toutes les icônes
- `.icon-xs`, `.icon-sm`, `.icon-md`, `.icon-lg`, `.icon-xl`, `.icon-2xl`, `.icon-3xl` - Tailles

### Classes de couleurs
- `.icon-primary`, `.icon-secondary`, `.icon-success`, `.icon-warning`, `.icon-danger`, `.icon-info`, `.icon-neutral`, `.icon-muted`

### Classes spécialisées
- `.icon-status` - Icônes de statut
- `.icon-badge` - Icônes avec fond gradient
- `.icon-trophy` - Icône trophée
- `.icon-star` - Icône étoile
- `.icon-chart` - Icône graphique
- `.icon-calendar` - Icône calendrier
- `.icon-homework` - Icône devoir
- `.icon-quiz` - Icône quiz
- `.icon-book` - Icône livre
- `.icon-document` - Icône document
- `.icon-check` - Icône coche
- `.icon-chat` - Icône chat
- `.icon-pen` - Icône crayon
- `.icon-bar-chart` - Icône graphique en barres
- `.icon-trending-up` - Icône tendance

## Bonnes pratiques

### ✅ À faire
- Utiliser les icônes simples pour une interface épurée
- Choisir des formes géométriques basiques pour les statistiques
- Utiliser des symboles universels (coche, étoile, cœur)
- Maintenir la cohérence visuelle avec des tailles appropriées

### ❌ À éviter
- Mélanger des icônes complexes avec des icônes simples
- Utiliser des icônes trop détaillées pour les petits formats
- Ignorer la hiérarchie visuelle des couleurs
- Surcharger l'interface avec trop d'icônes

## Avantages des icônes simples

### 🎯 **Lisibilité**
- Formes claires et reconnaissables
- Pas de détails qui distraient
- Compréhension immédiate

### 🚀 **Performance**
- SVG légers et rapides
- Pas de dépendances externes
- Rendu optimisé

### 🎨 **Cohérence**
- Style uniforme partout
- Palette de couleurs harmonieuse
- Tailles standardisées

### 🔧 **Maintenance**
- Code simple et lisible
- Modifications faciles
- Documentation claire

## Démonstration

Utilisez le composant `SimpleIconShowcaseWidget` pour voir toutes les icônes disponibles :

```tsx
import SimpleIconShowcaseWidget from '../components/widgets/SimpleIconShowcaseWidget';

<SimpleIconShowcaseWidget />
```

Ce composant affiche toutes les icônes simples avec leurs différentes tailles, couleurs et styles pour faciliter le développement et la maintenance.

## Migration depuis UnifiedIcon

Si vous souhaitez migrer depuis le système d'icônes unifié vers les icônes simples :

1. **Remplacer les imports** :
   ```tsx
   // Avant
   import UnifiedIcon from '../ui/UnifiedIcon';
   
   // Après
   import SimpleIcon from '../ui/SimpleIcon';
   ```

2. **Adapter les noms d'icônes** :
   ```tsx
   // Avant
   <UnifiedIcon name="checkCircle" size="lg" color="success" />
   
   // Après
   <SimpleIcon name="check" size="lg" color="success" />
   ```

3. **Tester l'affichage** pour s'assurer que les nouvelles icônes correspondent à vos besoins

Les icônes simples offrent une alternative épurée et moderne parfaitement adaptée aux interfaces minimalistes et professionnelles.

