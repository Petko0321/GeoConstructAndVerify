from sympy import symbols, groebner, simplify
import json
import itertools
import multiprocessing
import time

TIMEOUT = 1000

def compute_groebner(system1, current_gens, queue):
    try:
        gb1 = groebner(system1, *current_gens, domain="EX", order="lex")
        result = {
            "basis": [str(poly) for poly in gb1],
            "variables": [str(var) for var in gb1.gens],
            "order": str(gb1.order),
            "domain": str(gb1.domain),
        }
        queue.put(result)

    except Exception as e:
        queue.put({"error": str(e)})


def main():
    x1, y1, x2, y2, x3, y3, d6, d5, d4 = symbols("x1, y1, x2, y2, x3, y3, d6, d5, d4")
    list_of_gens = [[x1, y1], [x2, y2], [x3, y3], [d6], [d5], [d4]]

    # Зареждаме данни
    # with open(f"constructions\\geogebra\\construction1\\constr1_permutations_lex_order_data.json", "r") as f:
    #     orders = json.load(f)
    # list_of_priorities = orders["list of priorities"]
    # print(list_of_priorities)  
    
    with open(f"constructions\\geogebra\\construction1\\constr1_system.json", "r") as f:
        system1 = json.load(f)
    system1 = [simplify(expr) for expr in system1]
    print(system1)
    queue = multiprocessing.Queue()
    i = 0
    for perm in itertools.permutations(list_of_gens):
        current_gens = []
        for item in perm:
            if isinstance(item, list):
                current_gens.extend(item)
            else:
                current_gens.append(item)

        # Пропускаме комбинации, които вече са обработени
        # if current_gens in list_of_priorities:
        #     continue

        process = multiprocessing.Process(target=compute_groebner, args=(system1, current_gens, queue))

        start_time = time.time()
        process.start()
        process.join(TIMEOUT)

        if process.is_alive():
            print(f"⏱ Прекъсване: изчислението за {current_gens} отне повече от {TIMEOUT} секунди.")
            process.terminate()
            process.join()
            continue  

        end_time = time.time()
        elapsed_time = end_time - start_time

        if not queue.empty():
            result = queue.get()
            if "error" in result:
                print(f"⚠️ Грешка при изчисление за {current_gens}: {result['error']}")
                continue

            # Поставяме резултатите в изходния JSON
            gb_data3 = {
                "basis": result["basis"],
                "variables": result["variables"],
                "order": result["order"],
                "domain": result["domain"],
                "elapsed_time": float(elapsed_time)
            }

            with open(f"constructions\\geogebra\\construction1\\lex{i}.json", "w") as f:
                json.dump(gb_data3, f, indent=4)

            print(f"✅ Грьобнеровата база {i} е записана успешно за {elapsed_time:.2f} s! {current_gens}")
            i += 1
        else:
            print(f"⚠️ Няма резултат в опашката за {current_gens}.")


if __name__ == "__main__":
    main()




