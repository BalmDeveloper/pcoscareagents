from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional
import random

class DieticianAgent(PCOSAgent):
    """
    A specialized agent that provides personalized dietary recommendations for PCOS management.
    Focuses on improving insulin sensitivity, hormone balance, and overall health.
    """
    
    # Food categories with PCOS-specific recommendations
    FOOD_RECOMMENDATIONS = {
        "proteins": {
            "recommended": [
                "Fatty fish (salmon, mackerel, sardines)",
                "Poultry (chicken, turkey)",
                "Plant-based proteins (tofu, tempeh, edamame)",
                "Legumes (lentils, chickpeas, black beans)",
                "Eggs (especially omega-3 enriched)",
                "Lean meats (in moderation)",
                "Greek yogurt (unsweetened)",
                "Cottage cheese (low-fat)"
            ],
            "limit": [
                "Processed meats (sausages, bacon, deli meats)",
                "Fried meats",
                "Breaded or deep-fried proteins"
            ]
        },
        "carbohydrates": {
            "recommended": [
                "Non-starchy vegetables (leafy greens, broccoli, cauliflower, zucchini)",
                "Low-glycemic fruits (berries, apples, pears, citrus)",
                "Whole grains (quinoa, brown rice, oats, farro)",
                "Sweet potatoes (in moderation)",
                "Legumes (lentils, chickpeas, black beans)",
                "Chia seeds and flaxseeds"
            ],
            "limit": [
                "Refined grains (white bread, white rice, white pasta)",
                "Sugary foods and beverages",
                "Processed snacks and baked goods",
                "Sugary breakfast cereals"
            ]
        },
        "fats": {
            "recommended": [
                "Avocados",
                "Nuts and seeds (almonds, walnuts, chia, flax, pumpkin seeds)",
                "Olive oil and olives",
                "Fatty fish (salmon, mackerel, sardines)",
                "Nut butters (without added sugars)",
                "Coconut (in moderation)",
                "Dark chocolate (85% cocoa or higher)"
            ],
            "limit": [
                "Trans fats (partially hydrogenated oils)",
                "Excessive saturated fats",
                "Processed vegetable oils (soybean, corn, canola)"
            ]
        },
        "dairy_alternatives": {
            "recommended": [
                "Almond milk (unsweetened)",
                "Coconut milk (unsweetened)",
                "Oat milk (unsweetened, in moderation)",
                "Hemp milk",
                "Cashew milk"
            ],
            "limit": [
                "Sweetened non-dairy milks",
                "Flavored dairy products with added sugars"
            ]
        },
        "herbs_spices": {
            "recommended": [
                "Cinnamon (helps with blood sugar control)",
                "Turmeric (anti-inflammatory)",
                "Ginger (aids digestion)",
                "Fenugreek (may help with blood sugar)",
                "Cumin (aids digestion)",
                "Basil (anti-inflammatory)",
                "Oregano (antioxidant properties)",
                "Mint (aids digestion)",
                "Rosemary (antioxidant properties)",
                "Sage (may help with blood sugar)"
            ]
        }
    }
    
    # Sample meal plans by PCOS phenotype
    MEAL_PLANS = {
        "insulin_resistant": {
            "breakfast": [
                "Greek yogurt with berries, chia seeds, and walnuts",
                "Veggie omelet with avocado and whole grain toast",
                "Overnight oats with almond butter, flaxseeds, and cinnamon"
            ],
            "lunch": [
                "Grilled chicken salad with mixed greens, quinoa, and olive oil dressing",
                "Lentil soup with a side of roasted vegetables",
                "Quinoa bowl with roasted vegetables, chickpeas, and tahini dressing"
            ],
            "dinner": [
                "Baked salmon with roasted Brussels sprouts and sweet potato",
                "Turkey chili with kidney beans and a side of steamed broccoli",
                "Grilled tofu with stir-fried vegetables and brown rice"
            ],
            "snacks": [
                "Handful of almonds and an apple",
                "Carrot sticks with hummus",
                "Hard-boiled egg with cucumber slices"
            ]
        },
        "inflammatory": {
            "breakfast": [
                "Smoothie with spinach, berries, flaxseeds, and almond milk",
                "Chia pudding with walnuts and cinnamon",
                "Scrambled tofu with turmeric and vegetables"
            ],
            "lunch": [
                "Quinoa salad with mixed greens, avocado, and olive oil dressing",
                "Grilled salmon with steamed vegetables and quinoa",
                "Lentil and vegetable soup with a side of mixed greens"
            ],
            "dinner": [
                "Baked cod with roasted vegetables and quinoa",
                "Chickpea curry with brown rice and steamed greens",
                "Grilled chicken with roasted sweet potatoes and asparagus"
            ],
            "snacks": [
                "Handful of walnuts and blueberries",
                "Sliced apple with almond butter",
                "Celery sticks with tahini"
            ]
        },
        "adrenal": {
            "breakfast": [
                "Oatmeal with almond butter, chia seeds, and banana",
                "Smoothie with banana, spinach, almond butter, and flaxseeds",
                "Whole grain toast with avocado and poached eggs"
            ],
            "lunch": [
                "Quinoa bowl with roasted vegetables, chickpeas, and tahini dressing",
                "Grilled chicken wrap with whole grain tortilla and vegetables",
                "Lentil soup with a side of whole grain bread"
            ],
            "dinner": [
                "Baked salmon with quinoa and steamed vegetables",
                "Turkey meatballs with whole grain pasta and marinara sauce",
                "Grilled tofu with stir-fried vegetables and brown rice"
            ],
            "snacks": [
                "Greek yogurt with berries",
                "Handful of mixed nuts and dried fruit",
                "Rice cakes with almond butter"
            ]
        }
    }
    
    # PCOS-friendly recipes
    RECIPES = {
        "turmeric_golden_milk": {
            "name": "Anti-Inflammatory Turmeric Golden Milk",
            "ingredients": [
                "1 cup unsweetened almond milk (or coconut milk)",
                "1/2 tsp turmeric powder",
                "1/4 tsp cinnamon",
                "1/8 tsp ginger powder",
                "1/8 tsp black pepper (enhances curcumin absorption)",
                "1/2 tsp vanilla extract",
                "1/2 tsp honey or maple syrup (optional)",
                "Pinch of cardamom (optional)"
            ],
            "instructions": [
                "Whisk all ingredients together in a small saucepan over medium heat.",
                "Heat until hot but not boiling, about 3-5 minutes.",
                "Strain through a fine mesh strainer into a mug.",
                "Sprinkle with additional cinnamon if desired and serve warm."],
            "benefits": "Reduces inflammation, supports liver detoxification, and may help with insulin sensitivity.",
            "nutrition": {"calories": 50, "carbs": "5g", "fat": "3g", "protein": "1g"}
        },
        "quinoa_veggie_bowl": {
            "name": "PCOS Power Bowl with Quinoa and Roasted Vegetables",
            "ingredients": [
                "1 cup cooked quinoa",
                "1 cup mixed roasted vegetables (zucchini, bell peppers, broccoli)",
                "1/2 avocado, sliced",
                "1/4 cup chickpeas, drained and rinsed",
                "1 tbsp tahini",
                "1/2 lemon, juiced",
                "1 tbsp olive oil",
                "1/2 tsp cumin",
                "Salt and pepper to taste",
                "Fresh parsley for garnish"
            ],
            "instructions": [
                "In a bowl, combine cooked quinoa, roasted vegetables, chickpeas, and avocado.",
                "In a small bowl, whisk together tahini, lemon juice, olive oil, cumin, salt, and pepper.",
                "Drizzle the dressing over the bowl and toss gently to combine.",
                "Garnish with fresh parsley and serve."],
            "benefits": "High in fiber, plant-based protein, and healthy fats. Supports blood sugar balance and provides essential nutrients.",
            "nutrition": {"calories": 450, "carbs": "50g", "fat": "25g", "protein": "12g"}
        },
        "berry_smoothie": {
            "name": "Antioxidant Berry Smoothie",
            "ingredients": [
                "1 cup mixed berries (strawberries, blueberries, raspberries)",
                "1/2 banana (frozen)",
                "1 tbsp chia seeds",
                "1 tbsp almond butter",
                "1 cup unsweetened almond milk",
                "1/2 tsp cinnamon",
                "Handful of spinach (optional)",
                "Ice cubes (optional)"
            ],
            "instructions": [
                "Add all ingredients to a blender.",
                "Blend until smooth and creamy.",
                "Add more almond milk if needed to reach desired consistency.",
                "Pour into a glass and enjoy immediately."],
            "benefits": "Rich in antioxidants, fiber, and healthy fats. Supports hormone balance and reduces inflammation.",
            "nutrition": {"calories": 250, "carbs": "35g", "fat": "10g", "protein": "6g"}
        }
    }
    
    def __init__(self):
        super().__init__(
            name="Dietician Agent",
            description="Provides personalized dietary recommendations for PCOS management"
        )
        self.required_data = [
            'pcos_phenotype',
            'dietary_preferences',
            'food_allergies',
            'weight_goals',
            'current_diet'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Generate personalized dietary recommendations"""
        try:
            # Validate input data
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data for dietary recommendations: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Get PCOS phenotype (default to insulin resistant if not specified)
            phenotype = input_data.get('pcos_phenotype', 'insulin_resistant')
            
            # Generate personalized recommendations
            recommendations = self._generate_recommendations(phenotype, input_data)
            
            # Generate sample meal plan
            meal_plan = self._generate_meal_plan(phenotype, input_data)
            
            # Get recipe suggestions
            recipe_suggestions = self._get_recipe_suggestions(input_data)
            
            return AgentResponse(
                success=True,
                message="Dietary recommendations generated successfully",
                data={
                    "dietary_recommendations": recommendations,
                    "sample_meal_plan": meal_plan,
                    "recipe_suggestions": recipe_suggestions,
                    "helpful_tips": self._get_helpful_tips(phenotype)
                },
                next_steps=["fitness_agent", "obgyn"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error generating dietary recommendations: {str(e)}"
            )
    
    def _generate_recommendations(self, phenotype: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized dietary recommendations based on phenotype and preferences"""
        recommendations = {
            "general_guidelines": [
                "Eat balanced meals with protein, healthy fats, and fiber at each meal",
                "Choose low-glycemic index carbohydrates",
                "Include anti-inflammatory foods in your diet",
                "Stay hydrated with water and herbal teas",
                "Practice mindful eating and listen to hunger/fullness cues"
            ],
            "foods_to_include": [],
            "foods_to_limit": [],
            "lifestyle_recommendations": [
                "Aim for consistent meal timing",
                "Get regular physical activity",
                "Manage stress through relaxation techniques",
                "Prioritize quality sleep"
            ]
        }
        
        # Add phenotype-specific recommendations
        if phenotype == "insulin_resistant":
            recommendations["general_guidelines"].extend([
                "Pair carbohydrates with protein or healthy fats to slow glucose absorption",
                "Focus on high-fiber foods to improve insulin sensitivity"
            ])
            recommendations["foods_to_include"].extend([
                "Cinnamon (may help with blood sugar control)",
                "Apple cider vinegar (may improve insulin sensitivity)",
                "Chromium-rich foods (broccoli, green beans, nuts)"
            ])
            
        elif phenotype == "inflammatory":
            recommendations["general_guidelines"].extend([
                "Focus on anti-inflammatory foods",
                "Include omega-3 fatty acids regularly"
            ])
            recommendations["foods_to_include"].extend([
                "Turmeric and ginger (powerful anti-inflammatories)",
                "Fatty fish (salmon, mackerel, sardines)",
                "Colorful fruits and vegetables (rich in antioxidants)"
            ])
            
        elif phenotype == "adrenal":
            recommendations["general_guidelines"].extend([
                "Don't skip meals to maintain stable blood sugar",
                "Include protein with each meal and snack"
            ])
            recommendations["foods_to_include"].extend([
                "Magnesium-rich foods (leafy greens, nuts, seeds)",
                "Vitamin C-rich foods (citrus fruits, bell peppers)",
                "Complex carbohydrates for sustained energy"
            ])
        
        # Add personalized recommendations based on dietary preferences and restrictions
        if input_data.get('dietary_preferences'):
            if 'vegetarian' in input_data['dietary_preferences']:
                recommendations["foods_to_include"].extend([
                    "Plant-based protein sources (tofu, tempeh, legumes, quinoa)",
                    "Iron-rich plant foods with vitamin C to enhance absorption"
                ])
            if 'vegan' in input_data['dietary_preferences']:
                recommendations["foods_to_include"].extend([
                    "Algal oil or flaxseeds for omega-3s",
                    "Fortified plant milks and nutritional yeast for B12"
                ])
        
        # Add any food allergies to avoid
        if input_data.get('food_allergies'):
            recommendations["foods_to_avoid"] = input_data['food_allergies']
        
        return recommendations
    
    def _generate_meal_plan(self, phenotype: str, input_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate a sample meal plan based on phenotype"""
        # Get base meal plan for the phenotype
        meal_plan = {
            "breakfast": [],
            "morning_snack": [],
            "lunch": [],
            "afternoon_snack": [],
            "dinner": [],
            "evening_snack": []
        }
        
        # Select random meals for each category from the phenotype's meal plan
        if phenotype in self.MEAL_PLANS:
            for meal_time in ["breakfast", "lunch", "dinner"]:
                if meal_time in self.MEAL_PLANS[phenotype]:
                    meal_plan[meal_time] = random.sample(
                        self.MEAL_PLANS[phenotype][meal_time],
                        min(3, len(self.MEAL_PLANS[phenotype][meal_time]))
                    )
            
            # Add snacks
            if "snacks" in self.MEAL_PLANS[phenotype]:
                all_snacks = self.MEAL_PLANS[phenotype]["snacks"]
                meal_plan["morning_snack"] = random.sample(all_snacks, 2)
                meal_plan["afternoon_snack"] = random.sample([s for s in all_snacks if s not in meal_plan["morning_snack"]], 2)
                meal_plan["evening_snack"] = [s for s in all_snacks if s not in meal_plan["morning_snack"] + meal_plan["afternoon_snack"]][:1]
        
        # Customize based on dietary preferences
        if input_data.get('dietary_preferences'):
            if 'vegetarian' in input_data['dietary_preferences'] or 'vegan' in input_data['dietary_preferences']:
                # Replace animal proteins with plant-based alternatives
                for meal_time in meal_plan:
                    for i, meal in enumerate(meal_plan[meal_time]):
                        meal_plan[meal_time][i] = meal.replace('chicken', 'tofu')\
                            .replace('turkey', 'tempeh')\
                            .replace('salmon', 'chickpeas')\
                            .replace('fish', 'lentils')
        
        return meal_plan
    
    def _get_recipe_suggestions(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized recipe suggestions"""
        # In a real implementation, this would be more sophisticated
        # and match recipes to the user's preferences and needs
        return [
            {
                "name": self.RECIPES["turmeric_golden_milk"]["name"],
                "description": "A soothing anti-inflammatory drink",
                "prep_time": "5 min",
                "cook_time": "5 min"
            },
            {
                "name": self.RECIPES["quinoa_veggie_bowl"]["name"],
                "description": "A balanced meal with plant-based protein and healthy fats",
                "prep_time": "10 min",
                "cook_time": "20 min"
            },
            {
                "name": self.RECIPES["berry_smoothie"]["name"],
                "description": "Antioxidant-rich smoothie for hormone balance",
                "prep_time": "5 min",
                "cook_time": "0 min"
            }
        ]
    
    def _get_helpful_tips(self, phenotype: str) -> List[str]:
        """Get helpful tips specific to the PCOS phenotype"""
        tips = [
            "Stay hydrated by drinking plenty of water throughout the day",
            "Practice mindful eating by eating slowly and without distractions",
            "Include protein with each meal to help with satiety and blood sugar control"
        ]
        
        if phenotype == "insulin_resistant":
            tips.extend([
                "Try adding 1-2 tablespoons of apple cider vinegar to water before meals to help with blood sugar control",
                "Consider using smaller plates to help with portion control",
                "Aim for at least 25-30 grams of fiber per day"
            ])
        elif phenotype == "inflammatory":
            tips.extend([
                "Incorporate turmeric and ginger into your meals for their anti-inflammatory properties",
                "Consider an elimination diet if you suspect food sensitivities",
                "Focus on getting omega-3 fatty acids from fatty fish or flaxseeds"
            ])
        elif phenotype == "adrenal":
            tips.extend([
                "Don't skip meals to prevent blood sugar crashes",
                "Include a source of protein with each meal and snack",
                "Practice stress-reduction techniques like deep breathing or meditation"
            ])
            
        return tips
