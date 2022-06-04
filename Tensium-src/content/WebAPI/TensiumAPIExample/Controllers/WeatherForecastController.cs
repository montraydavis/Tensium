using Microsoft.AspNetCore.Mvc;

namespace TensiumAPIExample.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        public static Dictionary<string, WeatherForecast> WeatherForecasts { get; set; }

        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;

            if (WeatherForecasts == null)
            {
                var monday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(1),
                    Summary = "Very Hot Day!",
                    TemperatureC = 30
                };
                var tuesday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(2),
                    Summary = "Warm Day!",
                    TemperatureC = 21
                };
                var wednesday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(3),
                    Summary = "Cold Day!",
                    TemperatureC = 12
                };
                var thursday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(4),
                    Summary = "Very Cold Day!",
                    TemperatureC = 2
                };
                var friday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(5),
                    Summary = "Very Cold Day!",
                    TemperatureC = 3
                };
                var saturday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(6),
                    Summary = "Very Cold Day!",
                    TemperatureC = 1
                };
                var sunday = new WeatherForecast()
                {
                    Date = new DateTime().AddDays(7),
                    Summary = "Very Hot Day!",
                    TemperatureC = 37
                };

                WeatherForecasts = new Dictionary<string, WeatherForecast>()
                {
                    {nameof(monday), monday },
                    {nameof(tuesday), tuesday },
                    {nameof(wednesday), wednesday },
                    {nameof(thursday), thursday },
                    {nameof(friday), friday },
                    {nameof(saturday), saturday },
                    {nameof(sunday), sunday }
                };
            }
        }

        [HttpGet]
        public Dictionary<string, WeatherForecast> Get()
        {
            return WeatherForecasts;
        }

        [HttpPost]
        public Dictionary<string, WeatherForecast> Update([FromBody] WeatherForecast forecast)
        {

            var selected = WeatherForecasts.FirstOrDefault(x => x.Value.Id == forecast.Id);

            if(selected.Value != null)
            {
                WeatherForecasts[selected.Key] = forecast;
            }

            return WeatherForecasts;
        }
    }
}