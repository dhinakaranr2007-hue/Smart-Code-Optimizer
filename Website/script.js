const input = document.getElementById("input");
const nums = document.getElementById("nums");
const output = document.getElementById("out");

const run = document.getElementById("run");
const clear = document.getElementById("clear");

const validation = document.getElementById("valid");

const functionsEl = document.getElementById("f");
const loopsEl = document.getElementById("l");
const conditionsEl = document.getElementById("c");
const gainEl = document.getElementById("gain");

const toast = document.getElementById("toast");


// ============================================
// LINE NUMBERS
// ============================================

function updateLineNumbers() {

    const lines = input.value.split("\n");

    nums.innerHTML = lines
        .map((_, index) => `<div>${index + 1}</div>`)
        .join("");
}

input.addEventListener("input", updateLineNumbers);

input.addEventListener("scroll", () => {
    nums.scrollTop = input.scrollTop;
});

updateLineNumbers();


// ============================================
// TOAST MESSAGE
// ============================================

function showMessage(message) {

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(window.toastTimer);

    window.toastTimer = setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);
}


// ============================================
// BUTTON LOADING STATE
// ============================================

function setLoading(isLoading) {

    if (isLoading) {

        run.disabled = true;

        run.textContent =
            "◌  AI PROCESSING...";

    } else {

        run.disabled = false;

        run.textContent =
            "⚡ OPTIMIZE WITH AI →";
    }
}


// ============================================
// OPTIMIZE CODE
// ============================================

async function optimizeCode() {

    const code = input.value.trim();


    // Empty code check
    if (!code) {

        showMessage(
            "Please enter Python code first."
        );

        return;
    }


    // Loading state
    setLoading(true);


    // Update UI
    validation.textContent =
        "● ANALYZING";

    validation.className =
        "waiting";


    output.textContent =
        "AI is analyzing your code...\n\n" +
        "Connecting to Qwen2.5-Coder...\n\n" +
        "Please wait...";


    try {

        // ====================================
        // SEND CODE TO FLASK BACKEND
        // ====================================

        const response = await fetch(
            "/api/optimize",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    code: code
                })
            }
        );


        // Convert response to JSON
        const data =
            await response.json();


        // ====================================
        // BACKEND ERROR
        // ====================================

        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Optimization failed."
            );
        }


        // ====================================
        // DISPLAY ANALYSIS
        // ====================================

        const analysis =
            data.analysis || {};


        functionsEl.textContent =
            analysis.functions ?? 0;


        loopsEl.textContent =
            analysis.loops ?? 0;


        conditionsEl.textContent =
            analysis.conditions ?? 0;


        // ====================================
        // DISPLAY OPTIMIZED CODE
        // ====================================

        output.textContent =
            data.optimized_code ||
            "No optimized code returned.";


        // ====================================
        // VALIDATION
        // ====================================

        const validationResult =
            String(data.validation || "");


        if (
            validationResult
                .toLowerCase()
                .includes("pass")
        ) {

            validation.textContent =
                "● VALIDATION PASSED";

            validation.style.color =
                "#22c55e";

        } else {

            validation.textContent =
                "● VALIDATION CHECKED";

            validation.style.color =
                "#fbbf24";
        }


        // ====================================
        // PERFORMANCE
        // ====================================

        const performance =
            data.performance || {};


        const improvement =
            Number(
                performance.improvement_percentage
            );


        if (Number.isFinite(improvement)) {

            gainEl.textContent =
                improvement.toFixed(2) + "%";

        } else {

            gainEl.textContent =
                "—";
        }


        // ====================================
        // SUCCESS
        // ====================================

        showMessage(
            "✓ Code optimized successfully!"
        );


    } catch (error) {

        console.error(error);


        // Display error
        output.textContent =
            "OPTIMIZATION ERROR\n\n" +
            error.message;


        validation.textContent =
            "● ERROR";

        validation.style.color =
            "#fb7185";


        gainEl.textContent =
            "—";


        showMessage(
            "AI optimization failed."
        );


    } finally {

        setLoading(false);

    }
}


// ============================================
// BUTTON CLICK
// ============================================

run.addEventListener(
    "click",
    optimizeCode
);


// ============================================
// CLEAR BUTTON
// ============================================

clear.addEventListener(
    "click",
    () => {

        input.value = "";

        output.textContent =
            "Your optimized code will appear here...";


        functionsEl.textContent = "0";

        loopsEl.textContent = "0";

        conditionsEl.textContent = "0";

        gainEl.textContent = "—";


        validation.textContent =
            "● WAITING";

        validation.className =
            "waiting";

        validation.style.color =
            "";


        updateLineNumbers();


        showMessage(
            "Workspace cleared."
        );

    }
);


// ============================================
// CTRL + ENTER
// ============================================

input.addEventListener(
    "keydown",
    (event) => {

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            optimizeCode();
        }


        // TAB = 4 spaces
        if (event.key === "Tab") {

            event.preventDefault();


            const start =
                input.selectionStart;

            const end =
                input.selectionEnd;


            input.value =
                input.value.substring(
                    0,
                    start
                ) +
                "    " +
                input.value.substring(
                    end
                );


            input.selectionStart =
                input.selectionEnd =
                start + 4;


            updateLineNumbers();
        }

    }
);