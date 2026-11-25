import collections

class SimulatedAI:
    """
    Simulates an AI with a limited context window, demonstrating 'forgetfulness'.
    """
    def __init__(self, max_context_size=3):
        self.max_context_size = max_context_size
        # Using a deque for efficient FIFO operations (oldest context out)
        self.context = collections.deque(maxlen=max_context_size)
        self.relearn_events = 0

    def add_to_context(self, user_input):
        """Adds a new piece of information to the AI's context."""
        print(f"[Kullanıcı]: {user_input}")
        self.context.append(user_input)
        print(f"[AI Bağlamı]: {list(self.context)}")

    def query(self, user_query):
        """
        Simulates the AI attempting to answer a query based on its current context.
        If information is not in context, it's "forgotten".
        """
        print(f"\n[Kullanıcı Sorgusu]: {user_query}")
        
        # Simple check: does the query contain a keyword from the context?
        # In a real LLM, this would be much more complex, but for simulation, it works.
        found_in_context = False
        for item in self.context:
            if user_query.lower() in item.lower() or item.lower() in user_query.lower():
                found_in_context = True
                break

        if found_in_context:
            print(f"[AI Yanıtı]: Ah, evet, hatırlıyorum: '{user_query}' ile ilgili bilgi bağlamımda mevcut.")
            return True
        else:
            # This is where the "forgetfulness" and "idle session tax" manifest.
            # The AI asks for information to be re-stated, incurring a cost.
            print(f"[AI Yanıtı]: Üzgünüm, '{user_query}' hakkında bilgi bağlamımda bulamıyorum. Lütfen tekrar belirtir misiniz?")
            self.relearn_events += 1 # Increment the cost counter
            return False

# --- Demonstration ---
if __name__ == "__main__":
    print("--- Yapay Zeka Unutkanlığı Simülasyonu ---")
    print("AI'nın sınırlı bir hafızası (bağlam penceresi) vardır.")
    print("Bağlam dolduğunda, en eski bilgiler unutulur.\n")

    ai = SimulatedAI(max_context_size=3) # AI can remember 3 recent pieces of info

    # Initial interaction: User provides facts
    ai.add_to_context("Benim adım Ayşe.")
    ai.add_to_context("En sevdiğim renk mavi.")
    
    # AI can answer based on current context
    ai.query("Adın neydi?") # Should remember Ayşe
    ai.query("En sevdiğin renk neydi?") # Should remember mavi

    # Introduce new information, pushing older info out of the limited context window
    print("\n--- Bağlamı Doldurma ve Eski Bilgiyi Unutma ---")
    ai.add_to_context("Bugün hava çok güzel.") 
    ai.add_to_context("Yarın toplantım var.") # 'Benim adım Ayşe.' is now pushed out (max_context_size=3)
    
    # Test for forgotten information
    print("\n--- Unutulan Bilgiyi Sorgulama ---")
    if not ai.query("Adın neydi?"): # AI should now forget 'Ayşe'
        print("[Kullanıcı]: Adım Ayşe'ydi.")
        ai.add_to_context("Adım Ayşe.") # User has to re-state, incurring "Idle Session Tax"

    # AI now remembers 'Ayşe' again after re-statement
    ai.query("Adın neydi?")

    # Another piece of info to push out 'mavi'
    ai.add_to_context("Proje teslim tarihi Cuma.") # 'En sevdiğim renk mavi.' is now pushed out

    print("\n--- Başka Bir Unutma Örneği ---")
    if not ai.query("En sevdiğin renk neydi?"): # AI should now forget 'mavi'
        print("[Kullanıcı]: En sevdiğim renk maviydi.")
        ai.add_to_context("En sevdiğim renk mavi.") # User re-states

    print(f"\n--- Simülasyon Sonu ---")
    print(f"Toplam 'Boşta Oturum Vergisi' (yeniden öğrenme olayı): {ai.relearn_events}")
    print("Bu, kullanıcının AI'ya aynı bilgiyi tekrar tekrar sağlaması gereken durumları temsil eder.")
