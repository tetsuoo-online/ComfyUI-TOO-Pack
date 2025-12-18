import { app } from "../../scripts/app.js";

// Extension pour appliquer des couleurs personnalisées aux nœuds Comfyui-TOO-Pack
app.registerExtension({
    name: "comfyui-too-pack.appearance",
    async setup() {
        console.log("ComfyUI TOO Pack appearance extension setup");
    },
    
    async beforeRegisterNodeDef(nodeType, nodeData) {
        // Debug : afficher toutes les catégories pour voir leur structure exacte
        if (nodeData.category && nodeData.category.includes("TOO-Pack")) {
            console.log(`Category found: "${nodeData.category}" for node: ${nodeData.name}`);
        }
        
        // Vérifier si le nœud appartient à TOO-Pack
        if (nodeData.category && nodeData.category.includes("TOO-Pack")) {
            let backgroundColor = "#2E3B4E";  // Couleur bleu foncé par défaut | rose : #ad7591 - bleu clair : #7591ad
            let textColor = "#babacc";
            
            // Appliquer des couleurs différentes selon la sous-catégorie
            if (nodeData.category.includes("/image")) {
                backgroundColor = "#2E3B4E";  // Bleu-gris pour image
                textColor = "#babacc";
            } else if (nodeData.category.includes("/utils")) {
                backgroundColor = "#2d4e3b";  // Vert foncé pour utils
                textColor = "#babacc";
            } else if (nodeData.category.includes("/mixlab")) {
                backgroundColor = "#495b6c";  // bleu moyen pour mixlab
                textColor = "#babacc";
            }
            
            console.log(`Applying colors to: ${nodeData.name} - bg: ${backgroundColor}`);
            
            // Sauvegarder la fonction originale onNodeCreated
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // Modifier la fonction onNodeCreated
            nodeType.prototype.onNodeCreated = function() {
                if (onNodeCreated) {
                    onNodeCreated.apply(this, arguments);
                }
                
                // Appliquer les couleurs personnalisées
                this.bgcolor = backgroundColor;
                this.color = textColor;
                console.log(`Colors applied to: ${this.type} - bgcolor: ${this.bgcolor}`);
            };
        }
    }
});